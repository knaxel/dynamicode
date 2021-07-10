const SKULPT_ELEMENTS = {
    modules_registered: 0,
    modules_loaded: 0,
    running: false,
    instances: []
}


function set_run_buttons_status(disabled) {
    for (let i=0; i<SKULPT_ELEMENTS.instances.length; i++) {
        let instance = SKULPT_ELEMENTS.instances[i]
        instance.setButtonStatus(disabled, true)
    }
    SKULPT_ELEMENTS.running = disabled
}


function set_post_data(post) {
    Sk.postData = post
}


function registerModule(skulpt, name, url){
    SKULPT_ELEMENTS["modules_registered"] += 1
    let import_name = "src/lib/" + name + ".js"
    let request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.send(null);
    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            let type = request.getResponseHeader('Content-Type');
            if (type.indexOf("text") !== 1) {
                skulpt.externalLibraries[import_name] = request.responseText;
                SKULPT_ELEMENTS["modules_loaded"] += 1
                update_code_buttons()
            }
        }
    }
}



function builtinRead(x) {
    if (Sk.builtinFiles !== undefined && Sk.builtinFiles["files"][x] !== undefined) {
        return Sk.builtinFiles["files"][x]
    } else if (Sk.externalLibraries !== undefined && Sk.externalLibraries[x] !== undefined) {
        return Sk.externalLibraries[x]
    }
    throw "File not found: '" + x + "'"
}




function update_code_buttons() {
    let disabled = true
    if (skulptElementsAreSet()) {
        disabled = false
    }

    for (let i=0; i<SKULPT_ELEMENTS.instances.length; i++) {
        SKULPT_ELEMENTS.instances[i].setButtonStatus(disabled)
    }
}


class CodeRunner {
    constructor(codeEditorId, terminalEditorId, inputBarId, runButtonId, stopButtonId) {
        this.codeEditor = createSkulptInterface(codeEditorId)
        this.terminalEditor = createSkulptInterface(terminalEditorId, false)
        this.terminalScroll = $($($("#" + terminalEditorId).children()[0]).children()[1])
        this.inputBar = $("#" + inputBarId)
        this.runButton = $("#" + runButtonId)
        this.stopButton = $("#" + stopButtonId)

        this.running = false

        this.inputBar.hide()
        this.stopButton.hide()

        this.runButton.on("click", () => this.run(this))
        this.stopButton.on("click", () => this.stop(this))
        if (!skulptElementsAreSet()) {
            this.runButton.prop("disabled", true)
            this.stopButton.prop("disabled", true)
        }
        SKULPT_ELEMENTS.instances.push(this)
    }

    run(codeRunnerInstance) {
        if (codeRunnerInstance.running || SKULPT_ELEMENTS.running) {
            return
        }
        codeRunnerInstance.runButton.hide()
        codeRunnerInstance.stopButton.show()
        codeRunnerInstance.terminalEditor.doc.setValue("")

        Sk.configure({
            output: (text) => codeRunnerInstance.print(text, codeRunnerInstance),
            read: builtinRead,
            inputfun: () => codeRunnerInstance.getUserInput(codeRunnerInstance)
        })

        let code = codeRunnerInstance.codeEditor.doc.getValue()
        Sk.misceval.asyncToPromise(function() {
            return Sk.importMainWithBody("<stdin>", false, code, true)
        }).then(function(mod) {
            codeRunnerInstance.running = false
            codeRunnerInstance.runButton.show()
            codeRunnerInstance.stopButton.hide()
            set_run_buttons_status(false)
        }, function(err) {
            codeRunnerInstance.print(err.toString() + "\n", codeRunnerInstance)
            codeRunnerInstance.running = false
            codeRunnerInstance.runButton.show()
            codeRunnerInstance.stopButton.hide()
            set_run_buttons_status(false)
        });
        codeRunnerInstance.running = true
        set_run_buttons_status(true)
    }

    stop(codeRunnerInstance) {
        if (!codeRunnerInstance.running) {
            return
        }
        Sk.timeoutMsg = function() {
            Sk.execLimit = Infinity
            codeRunnerInstance.running = false
            codeRunnerInstance.stopButton.hide()
            codeRunnerInstance.runButton.show()
            set_run_buttons_status(false)
        }
        Sk.execLimit = 1
        codeRunnerInstance.inputBar.trigger("keyup")
        if (Sk.sleepResolver !== undefined) {
            Sk.sleepResolver(Sk.builtin.none.none)
            Sk.sleepResolver = undefined
            if (Sk.sleepTimeoutIdentifier) {
                clearTimeout(Sk.sleepTimeoutIdentifier)
                Sk.sleepTimeoutIdentifier = undefined
            }
        }
    }

    print(text, codeRunnerInstance=null) {
        if (codeRunnerInstance === null) {
            codeRunnerInstance = this
        }
        let prev_value = codeRunnerInstance.terminalEditor.doc.getValue()
        codeRunnerInstance.terminalEditor.doc.setValue(prev_value + text.toString())

        codeRunnerInstance.terminalScroll.scrollTop(codeRunnerInstance.terminalScroll[0].scrollHeight);
    }

    getUserInput(codeRunnerInstance) {
        return new Promise(function(resolve, reject){
            codeRunnerInstance.inputBar.val("")
            codeRunnerInstance.inputBar.show()
            codeRunnerInstance.inputBar.focus()
            let active = true
            codeRunnerInstance.inputBar.on("keyup",function(e){
                if (e.keyCode === 13 || Sk.execLimit === 1) {
                    codeRunnerInstance.inputBar.off("keyup")
                    codeRunnerInstance.inputBar.hide()
                    let text = codeRunnerInstance.inputBar.val()
                    active = false
                    codeRunnerInstance.print(text + "\n", codeRunnerInstance)
                    resolve(text);
                }
            })
        })
    }

    setButtonStatus(isDisabled, justRunButton=false) {
        this.runButton.prop("disabled", isDisabled)
        if (!justRunButton) {
            this.stopButton.prop("disabled", isDisabled)
        }
    }

    setEditorSize(width, height) {
        this.codeEditor.setSize(width, height)
        this.terminalEditor.setSize(width, height)
    }
}


function skulptElementsAreSet() {
    return SKULPT_ELEMENTS["modules_registered"] === SKULPT_ELEMENTS["modules_loaded"];
}


function createSkulptInterface(divId, isCodeInput=true) {
    let config = {
        lineNumbers: true,
        mode: "python",
        theme: "darcula"
    }
    if (!isCodeInput) {
        config = {
            lineNumbers: false,
            theme: "base16-dark",
            readOnly: true,
            mode: "text",
            cursorBlinkRate: -1
        }
    }

    return CodeMirror(document.getElementById(divId), config)
}


delete Sk.builtinFiles.files["src/lib/document.js"]


Sk.externalLibraries = {}
registerModule(Sk, "post", "/static/js/skulpt_custom_modules/post/__init__.js")
