
function load_post(divId, json_data) {
    let post = new Post(divId, json_data["title"], json_data["author"])
    for (let i=0; i<json_data["blocks"].length; i++) {
        post.create_block(json_data["blocks"][i])
    }
    set_post_data(post)
}


function get_code_block(name) {
    return $(`<div class="code-block mt-3 mb-3">
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


function render_options(choices) {
    let options = ""

    for (let i=0; i<choices.length; i++) {
        let option = `<option value="${choices[i]}">${choices[i]}</option>`
        options = options + "\n" + option
    }

    return options
}


class Post {
    constructor(parentDivId, title, author) {
        this.title = title
        this.author = author
        this.blocks = []

        this.parentDiv = $(`#${parentDivId}`)
        this.parentDiv.append($(`<h2>${title}</h2>`))
        this.parentDiv.append($(`<p>${author}</p>`))
    }

    add_block(block) {
        this.blocks.push(block)
    }

    get_block(block_name) {
        for (let i=0; i<this.blocks.length; i++) {
            if (this.blocks[i].get_name() === block_name) {
                return this.blocks[i]
            }
        }
        return undefined
    }

    create_block(json_data) {
        let type = json_data["type"]
        if (type === "TextBlock") {
            let block = new TextBlock(this, json_data["name"], json_data["text"])
            this.add_block(block)
        } else if(type === "CodeBlock") {
            let block = new CodeBlock(this, json_data["name"], json_data["code"])
            this.add_block(block)
        } else if(type === "ChoiceBlock") {
            let block = new ChoiceBlock(this, json_data["name"], json_data["choices"],
                json_data["text"])
            this.add_block(block)
        }
    }
}


class Block {
    constructor(parentPost, name, isCodeBlock=false) {
        this.parentPost = parentPost
        this.name = name
        if (isCodeBlock) {
            this.containerDiv = $("<div class=\"post-code-block-container\"></div>")
        } else {
            this.containerDiv = $(`<div class="post-block-container"><b>Block ${name}</b></div>`)
        }
        this.parentPost.parentDiv.append(this.containerDiv)

        this.hidden = false
    }

    is_hidden() {
        return this.hidden
    }

    show() {
        if (this.is_hidden()) {
            this.containerDiv.show()
            this.hidden = false
        }
    }

    hide() {
        if (!this.is_hidden()) {
            this.containerDiv.hide()
            this.hidden = true
        }
    }

    set_name(new_name) {
        this.name = new_name
    }

    get_name() {
        return this.name
    }
}


class TextBlock extends Block {
    constructor(parentPost, name, text) {
        super(parentPost, name);
        this.textDiv = $(`<div>${text}</div>`)
        this.containerDiv.append(this.textDiv)
    }

    set_text(new_text) {
        this.textDiv.text(new_text)
    }

    get_text() {
        return this.textDiv.text()
    }
}


class CodeBlock extends Block {
    constructor(parentPost, name, code) {
        super(parentPost, name, true);
        this.codeRunnerDiv = get_code_block(name)
        this.containerDiv.append(this.codeRunnerDiv)

        this.codeRunner = new CodeRunner(`codeEditor${name}`, `outputEditor${name}`,
            `inputBar${name}`, `runButton${name}`, `stopButton${name}`)
        set_resize_buttons(this.codeRunner, `expandEditorButton${name}`,
            `shortenEditorButton${name}`, `expandConsoleButton${name}`,
            `shortenConsoleButton${name}`)
        this.codeRunner.codeEditor.doc.setValue(code)
    }
}


class ChoiceBlock extends TextBlock {
    constructor(parentPost, name, choices, text) {
        super(parentPost, name, text)
        this.choices = choices
        this.selectDiv = $(`<select class="form-control block-select mt-2">${render_options(choices)}</select>`)
        this.containerDiv.append(this.selectDiv)
    }

    get_choices() {
        return this.choices
    }

    get_selected() {
        return this.selectDiv.val()
    }
}
