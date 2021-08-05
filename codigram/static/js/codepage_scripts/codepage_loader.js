const MARKDOWN = new showdown.Converter()


function load_codepage(divId, json_data) {
    reset_skulpt_instances()
    let codepage = new CodePage(divId, json_data["title"], json_data["author"], json_data["author_uuid"], json_data["date_created"])
    for (let i=0; i<json_data["blocks"].length; i++) {
        codepage.create_block_json(json_data["blocks"][i])
    }
    set_codepage_data(codepage)
    return codepage
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
        let option = `<option value="${choices[i]}">${choices[i]}</option>`
        options = options + "\n" + option
    }

    return options
}

//renaming this to CodePage since its the same code being used for the sandbox
class CodePage {
    constructor(parentDivId, title, author, author_uuid, date_created) {

        this.title = title
        this.author = author
        this.author_uuid = author_uuid
        this.date_created = date_created
        this.raw_blocks = []
        this.blocks_by_name = {}
        this.blocks = []

        this.parentDivId = parentDivId
        this.parentDiv = $(`#${this.parentDivId}`)
        this.parentDiv.append($(`<h2 class="codepage_title ps-1">${this.title}</h2>`))
        this.parentDiv.append($(`
            <p class="codepage_author ps-1 mt-2">
            Created by <a class="a-underline" href="/user_profile/${this.author_uuid}">${this.author}</a> on ${this.date_created}
            </p>`))
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
            let args = [this.parentDivId, js_block["name"], js_block["text"]]
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
            self.container_div = $(`<div class="codepage-block-container rounded-3 bg-light mb-3"><span class="block-label">${self.type} Block: ${name}</span></div>`)
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

        self.text_div = $(`<div></div>`)
        self.text_div.html(MARKDOWN.makeHtml(text))
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

let imageBlockClass = Sk.misceval.buildClass({}, function($glb, $loc) {
    $loc.type = new Sk.builtin.str("Image")

    $loc.__init__ = new Sk.builtin.func(function(self, parent_codepage, name, text, src) {
        let super_class = get_sk_super(self, "ImageBlock")
        super_class.__init__.tp$call([self, parent_codepage, name, text])  // Equivalent to super().__init__(...)


        set_class_var(self, "src", new Sk.builtin.str(src))

        self.img = $(`<img class=" d-block mx-auto block-select mt-2" width="300" src="${src}" onerror="this.onerror=null;this.src = \'https://developers.google.com/maps/documentation/maps-static/images/error-image-generic.png\'"/>`)
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

    $loc.__init__ = new Sk.builtin.func(function(self, parent_codepage, name, text) {
        let super_class = get_sk_super(self, "SliderBlock")
        super_class.__init__.tp$call([self, parent_codepage, name, text])  // Equivalent to super().__init__(...)



        self.slider = $(`<input type="range" class="form-range bg-light rounded-bottom p-4" step=".01"/>`)
        self.container_div.append(self.slider)
        set_class_var(self, "range", new Sk.builtin.float_(self.slider.val() ))
    })


    $loc.get_value = new Sk.builtin.func(function(self) {
        return new Sk.builtin.float_( self.slider.val())
    })
}, "SliderBlock", [textBlockClass])

