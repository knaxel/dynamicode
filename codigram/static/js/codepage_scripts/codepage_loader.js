
function load_codepage(divId, json_data, editable) {
    let codepage = new CodePage(divId, json_data["title"], json_data["author"], editable)
    for (let i=0; i<json_data["blocks"].length; i++) {
        codepage.create_block_json(json_data["blocks"][i])
    }
    if (json_data["blocks"].length === 0) {
        codepage.create_drag_destination()
    }
    set_codepage_data(codepage)
    return codepage
}


function html_codeblock(name) {
    return $(`
        <div class="code-block mt-3 mb-3">
            <div class="code-block-controller d-flex justify-content-between">
                <div>
                    <button class="code-control-button play-button" id="runButton${name}"></button>
                    <button class="code-control-button stop-button" id="stopButton${name}"></button>
                    <button class="code-control-name">Block ${name}</button>
                </div>
                <div>
                    <button class="code-control-resize" id="expandEditorButton${name}">Expand Editor</button>
                    <button class="code-control-resize" id="shortenEditorButton${name}">Shorten Editor</button>
                    <button class="code-control-resize" id="expandConsoleButton${name}">Expand Console</button>
                    <button class="code-control-resize" id="shortenConsoleButton${name}">Shorten Console</button>
                </div>
            </div>

            <div id="codeEditor${name}"></div>
            <div id="outputEditor${name}"></div>
            <input class="input-bar" id="inputBar${name}" placeholder="Type here">
        </div>`)
}


function html_options(choices) {
    let options = ""

    for (let i=0; i<choices.length; i++) {
        let option = `<option value="${choices[i]}">${choices[i]}</option>`
        options = options + "\n" + option
    }

    return options
}

//renaming this to CodePage since its the same code being used for the sandbox
class CodePage {
    constructor(parentDivId, title, author, editable) {

        this.title = title
        this.author = author
        this.editable = editable
        this.raw_blocks = []
        this.blocks_by_name = {}
        this.blocks = []

        this.parentDivId = parentDivId
        this.parentDiv = $(`#${this.parentDivId}`)
        this.parentDiv.append($(`<h2 class="codepage_title ps-1">${this.title}</h2>`))
        this.parentDiv.append($(`<p class="codepage_author ps-1 mt-2"> - ${this.author}</p>`))
    }

    add_block(name, block) {
        this.raw_blocks.push(block)
        this.blocks = new Sk.builtin.list(this.raw_blocks)
        this.blocks_by_name[name] = block
    }

    get_block(block_name) {
        return this.blocks_by_name[block_name]
    }

    create_new_block(type, name, ...content){
        console.log(content)
        if (type === "TextBlock") {
            let args = [this.parentDivId, name, content[0]]
            let python_block = textBlockClass.tp$call(args)
            this.add_block(name, python_block)
        } else if(type === "CodeBlock") {
            let args = [this.parentDivId, name, content[0]]
            let python_block = codeBlockClass.tp$call(args)
            this.add_block(name, python_block)
        } else if(type === "ChoiceBlock") {
            let args = [this.parentDivId, name, content[0] ,content[1]]
            let python_block = choiceBlockClass.tp$call(args)
            this.add_block(name, python_block)
        }
    }

    create_block_json(js_block) {
        let type = js_block["type"]
        if (type === "TextBlock") {
            let args = [this.parentDivId, js_block["name"], js_block["text"]]
            let python_block = textBlockClass.tp$call(args)
            this.add_block(js_block["name"], python_block)
        } else if(type === "CodeBlock") {
            let args = [this.parentDivId, js_block["name"], js_block["code"]]
            let python_block = codeBlockClass.tp$call(args)
            this.add_block(js_block["name"], python_block)
        } else if(type === "ChoiceBlock") {
            let args = [this.parentDivId, js_block["name"], js_block["text"], js_block["choices"]]
            let python_block = choiceBlockClass.tp$call(args)
            this.add_block(js_block["name"], python_block)
        }
    }

    create_drag_destination() {
        let drag_target = $("<div id='singleDragTarget'></div>")
        drag_target.ondrop((event) => {
            event.preventDefault()
            let data = event.dataTransfer.getData("text")
            $(event.target).append($("<p>Test</p>"))
        })
        drag_target.
        this.parentDiv.append(drag_target)
    }
}


function set_class_var(self, var_name, var_value) {
    self.$d.entries[var_name] = [
    new Sk.builtin.str(var_name),
    var_value
    ]
}


function get_class_var(self, var_name) {
    return self.$d.entries[var_name][1]
}


function get_sk_super(self, name) {
    if (self) {
        if (self.hasOwnProperty("tp$name") && self.tp$name === name) {
            return Object.getPrototypeOf(self)
        } else {
            return get_sk_super(Object.getPrototypeOf(self), name)
        }
    }
}


let blockClass = Sk.misceval.buildClass({}, function($glb, $loc) {
    $loc.type = Sk.builtin.none.none$

    $loc.__init__ = new Sk.builtin.func(function(self, codepage_div_id, name, isCodeBlock) {
        self.codepage_div = $(`#${codepage_div_id}`)
        set_class_var(self, "name", new Sk.builtin.str(name))

        if (isCodeBlock) {
            self.container_div = $("<div class=\"codepage-code-block-container rounded-3\"></div>")
        } else {
            self.container_div = $(`<div class="codepage-block-container rounded-3 bg-light p-3"><b>Block - ${name}</b></div>`)
        }
        self.codepage_div.append(self.container_div)
    })

    $loc.is_hidden = new Sk.builtin.func(function(self) {
        if (self.container_div.is(":hidden")) {
            return Sk.builtin.bool.true$
        } else {
            return Sk.builtin.bool.false$
        }
    })

    $loc.show = new Sk.builtin.func(function(self) {
        if (self.container_div.is(":hidden")) {
            self.container_div.show()
        }
    })

    $loc.hide = new Sk.builtin.func(function(self) {
        if (!self.container_div.is(":hidden")) {
            self.container_div.hide()
        }
    })

}, "Block", [])


let textBlockClass = Sk.misceval.buildClass({}, function($glb, $loc) {
    $loc.type = new Sk.builtin.str("Text")

    $loc.__init__ = new Sk.builtin.func(function(self, parent_codepage, name, text) {
        let super_class = get_sk_super(self, "TextBlock")
        super_class.__init__.tp$call([self, parent_codepage, name, false])  // Equivalent to super().__init__(...)

        self.text_div = $(`<div>${text}</div>`)
        self.container_div.append(self.text_div)
    })

    $loc.set_text = new Sk.builtin.func(function(self, new_text) {
        self.text_div.text(new_text)
    })

    $loc.get_text = new Sk.builtin.func(function(self, ) {
        return new Sk.builtin.str(self.text_div.text())
    })
}, "TextBlock", [blockClass])


let codeBlockClass = Sk.misceval.buildClass({}, function($glb, $loc) {
    $loc.type = new Sk.builtin.str("Code")

    $loc.__init__ = new Sk.builtin.func(function(self, parent_codepage, name, code) {
        let super_class = get_sk_super(self, "CodeBlock")
        super_class.__init__.tp$call([self, parent_codepage, name, true])  // Equivalent to super().__init__(...)

        self.code_runner_div = html_codeblock(name)
        self.container_div.append(self.code_runner_div)

        self.code_runner = new CodeRunner(`codeEditor${name}`, `outputEditor${name}`,
            `inputBar${name}`, `runButton${name}`, `stopButton${name}`)
        set_resize_buttons(self.code_runner, `expandEditorButton${name}`,
            `shortenEditorButton${name}`, `expandConsoleButton${name}`,
            `shortenConsoleButton${name}`)
        self.code_runner.codeEditor.doc.setValue(code)
    })

}, "CodeBlock", [blockClass])


let choiceBlockClass = Sk.misceval.buildClass({}, function($glb, $loc) {
    $loc.type = new Sk.builtin.str("Choice")

    $loc.__init__ = new Sk.builtin.func(function(self, parent_codepage, name, text, choices) {
        let super_class = get_sk_super(self, "ChoiceBlock")
        super_class.__init__.tp$call([self, parent_codepage, name, text])  // Equivalent to super().__init__(...)

        console.log(choices)
        let python_choices = []
        for (let i=0; i<choices.length; i++) {
            python_choices.push(new Sk.builtin.str(choices[i]))
        }
        python_choices = new Sk.builtin.list(python_choices)
        set_class_var(self, "choices", python_choices)

        self.select_div = $(`<select class="form-control block-select mt-2">${html_options(choices)}</select>`)
        self.container_div.append(self.select_div)
    })

    $loc.get_selected_choice = new Sk.builtin.func(function(self) {
        return new Sk.builtin.str(self.select_div.val())
    })

}, "ChoiceBlock", [textBlockClass])

