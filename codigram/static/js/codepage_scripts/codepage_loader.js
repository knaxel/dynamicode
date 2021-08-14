const MARKDOWN = new showdown.Converter()


function load_codepage(divId, json_data, show_edit=false) {
    reset_skulpt_instances()
    let codepage = new CodePage(divId, show_edit, json_data["title"], json_data["author"], json_data["author_uuid"],
        json_data["date_created"], json_data["date_edited"])
    for (let i=0; i<json_data["blocks"].length; i++) {
        codepage.create_block_json(json_data["blocks"][i])
    }
    set_codepage_data(codepage)
    return codepage
}


function htmlUnsafe(safe_string) {
    return String(safe_string).replace(/&amp;/g, '&').replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>').replace(/&quot;/g, '"')
        .replace(/&#34;/g, '"').replace(/&#39;/g, "'");
}


function htmlSafe(unsafe_string) {
    return String(unsafe_string).replace(/&/g, '&amp;')
        .replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}


function makeMarkdown(textString) {
    return MARKDOWN.makeHtml(textString)
}


function allowUnsafeInCodeElements(parent) {
    let elements = parent.find("code")
    elements.each(function() {
        let elem = $(this)
        let innerText = elem.text()
        innerText = htmlUnsafe(innerText)
        elem.text(innerText)
    })
}


function html_codeblock(name) {
    return $(`
        <div class="code-block mt-3 mb-3">
            <div class="code-block-controller d-flex justify-content-between">
                <div>
                    <button class="code-control-button play-button" data-block-id="runButton${name}"></button>
                    <button class="code-control-button stop-button" data-block-id="stopButton${name}"></button>
                    <span class="code-control-name">Code Block: ${name}</span>
                </div>
                <div>
                    <button class="code-control-resize" data-block-id="expandEditorButton${name}">Expand Editor</button>
                    <button class="code-control-resize" data-block-id="shortenEditorButton${name}">Shorten Editor</button>
                    <button class="code-control-resize" data-block-id="expandConsoleButton${name}">Expand Console</button>
                    <button class="code-control-resize" data-block-id="shortenConsoleButton${name}">Shorten Console</button>
                </div>
            </div>

            <div data-block-id="codeEditor${name}"></div>
            <div data-block-id="outputEditor${name}"></div>
            <input class="input-bar" data-block-id="inputBar${name}" placeholder="Type here">
        </div>`)
}


function html_options(choices) {
    let options = ""

    for (let i=0; i<choices.length; i++) {
        let choice = htmlSafe(choices[i])
        let option = `<option value="${choice}">${choice}</option>`
        options = options + "\n" + option
    }

    return options
}

//renaming this to CodePage since its the same code being used for the sandbox
class CodePage {
    constructor(parentDivId, show_edit, title, author, author_uuid, date_created, date_edited) {

        this.title = title
        this.author = author
        this.author_uuid = author_uuid
        this.date_created = date_created
        this.date_edited = date_edited
        this.raw_blocks = []
        this.blocks_by_name = {}
        this.blocks = []

        this.parentDivId = parentDivId
        this.parentDiv = $(`#${this.parentDivId}`)
        if (show_edit) {
            this.parentDiv.append($(`<h2 class="ps-1"><span class="codepage-title">${this.title}</span><a class="fas fa-pencil-alt h4 codepage-edit" href="${EDIT_URL}"></a></h2>`))
        } else {
            this.parentDiv.append($(`<h2 class="ps-1">${this.title}</h2>`))
        }

        let extraClass = ""
        if (!this.date_edited) {extraClass = "mb-2"}
        this.parentDiv.append($(`
            <div class="codepage-author ps-1 mt-2 small ${extraClass}">
            Created by <a class="codepage-author a-underline" href="/user_profile/${this.author_uuid}">${this.author}</a> on ${this.date_created}
            </div>`))
        if (this.date_edited) {
            this.parentDiv.append($(`
                <div class="codepage-author ps-1 mb-2 small">
                Last edited on ${this.date_edited}
                </div>`))
        }
    }

    add_block(name, block) {
        this.raw_blocks.push(block)
        this.blocks = new Sk.builtin.list(this.raw_blocks)
        this.blocks_by_name[name] = block
    }

    get_block(block_name) {
        return this.blocks_by_name[block_name]
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
        } else if(type === "ImageBlock") {
            let args = [this.parentDivId, js_block["name"], js_block["text"], js_block["src"]]
            let python_block = imageBlockClass.tp$call(args)
            this.add_block(js_block["name"], python_block)
        } else if(type === "SliderBlock") {
            let args = [this.parentDivId, js_block["name"], js_block["text"],
                js_block["lower"], js_block["upper"], js_block["default"]]
            let python_block = sliderBlockClass.tp$call(args)
            this.add_block(js_block["name"], python_block)
        }
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
            self.container_div = $(`<div class="codepage-code-block-container rounded-3"></div>`)
        } else {
            self.container_div = $(`<div class="codepage-block-container rounded-3 bg-light mb-3"><span class="block-label">${self.type} Block: ${htmlSafe(name)}</span></div>`)
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

        self.text = text
        self.text_div = $(`<div class="max-width-100"></div>`)
        self.text_div.html(makeMarkdown(htmlSafe(self.text)))
        allowUnsafeInCodeElements(self.text_div)
        self.container_div.append(self.text_div)
    })

    $loc.set_text = new Sk.builtin.func(function(self, new_text) {
        console.log("here")
        self.text = new_text.toString()
        self.text_div.html(makeMarkdown(htmlSafe(self.text)))
        allowUnsafeInCodeElements(self.text_div)
    })

    $loc.get_text = new Sk.builtin.func(function(self) {
        return new Sk.builtin.str(self.text)
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

        let python_choices = []
        for (let i=0; i<choices.length; i++) {
            python_choices.push(new Sk.builtin.str(htmlSafe(choices[i])))
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

let imageBlockClass = Sk.misceval.buildClass({}, function($glb, $loc) {
    $loc.type = new Sk.builtin.str("Image")

    $loc.__init__ = new Sk.builtin.func(function(self, parent_codepage, name, text, src) {
        let super_class = get_sk_super(self, "ImageBlock")
        super_class.__init__.tp$call([self, parent_codepage, name, text])  // Equivalent to super().__init__(...)


        set_class_var(self, "src", new Sk.builtin.str(src))

        self.img = $(`<img class=" d-block mx-auto block-select mt-2 max-width-100" src="${encodeURI(src)}"/>`)
        self.container_div.append(self.img)
    })


    $loc.get_src = new Sk.builtin.func(function(self) {
        return new Sk.builtin.str( $(self.img).attr("src"))
    })
    $loc.set_src = new Sk.builtin.func(function(self, new_src) {
        $(self.img).attr("src", new_src+"?t="+ new Date().getTime());
    })
}, "ImageBlock", [textBlockClass])

let sliderBlockClass = Sk.misceval.buildClass({}, function($glb, $loc) {
    $loc.type = new Sk.builtin.str("Slider")

    $loc.__init__ = new Sk.builtin.func(function(self, parent_codepage, name, text, lower, upper, defaultValue) {
        let super_class = get_sk_super(self, "SliderBlock")
        super_class.__init__.tp$call([self, parent_codepage, name, text])  // Equivalent to super().__init__(...)

        self.lower = lower
        self.upper = upper
        self.defaultValue = defaultValue

        let labels = $(`<div class="d-flex justify-content-between"></div>`)
        labels.append($(`<span class="text-left slider-label left">${self.lower}</span>`))
        self.valueLabel = $(`<span class="text-center slider-label center bg-dark rounded-5">${self.defaultValue}</span>`)
        labels.append(self.valueLabel)
        labels.append($(`<span class="text-right slider-label right">${self.upper}</span>`))

        self.slider = $(`<input type="range" class="form-range bg-light rounded-bottom p-4" step=".01"/>`)
        self.container_div.append(labels)
        self.container_div.append(self.slider)

        self.slider.on("input", () => {
            let value = (parseFloat(self.slider.val())/100) * (self.upper - self.lower) + self.lower
            self.value = parseFloat(value)
            self.valueLabel.text(Math.round(self.value))
        })
        self.value = defaultValue
        self.slider.val((defaultValue - self.lower) / (self.upper - self.lower) * 100)

        set_class_var(self, "lower", new Sk.builtin.float_(self.lower))
        set_class_var(self, "upper", new Sk.builtin.float_(self.lower))
        set_class_var(self, "default", new Sk.builtin.float_(self.lower))
    })


    $loc.get_value = new Sk.builtin.func(function(self) {
        let rounded = Math.round((self.value + Number.EPSILON) * 100) / 100
        return new Sk.builtin.float_(rounded)
    })
}, "SliderBlock", [textBlockClass])

