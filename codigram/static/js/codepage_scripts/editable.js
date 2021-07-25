
function load_editable_codepage(parentDivId, json_data) {
    let editableCodepage = new EditableCodePage(parentDivId, json_data)
    if (json_data["blocks"].length === 0) {
        editableCodepage.createTopDragTarget()
    }

    let draggables = $("a[data-block-adder]")
    draggables.draggable({
        revert: true,
        revertDuration: 0,
        cursorAt: {left: 60, top: 60}
    })
    return editableCodepage
}


function generateName(i) {
    let alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if (i < 26) {
        return alphabet[i]
    }
    return generateName(Math.floor(i/26)-1) + alphabet[i%26]
}


class EditableCodePage {
    constructor(parentDivId, json_data) {
        this.parentDivId = parentDivId
        this.parentDiv = $(`#${parentDivId}`)
        this.data = json_data

        this.titleDiv = $(`
            <div class='rounded-5 input-group p-0 shadow-sm mb-3' data-children-count='1'>
            <button class='btn btn-lg shadow-none rounded-5 bg-extra-light text-dark pe-3 h3 m-0 text-white' type='button'>Title</button>
            <input id='editableTitle' type='text' style='flex:1 1 auto;' class='h3 border-0 bg-light rounded-5 m-0 ps-3 p-1' placeholder='Sandbox Title' value='${this.data["title"]}'>
            </div>"`)

        this.parentDiv.append(this.titleDiv)
        this.titleInput = $("#editableTitle")
        this.titleInput.on("keyup", (key) => {
            if (this.titleInput.val()) {
                this.data["title"] = this.titleInput.val()
            }
        })
        this.titleInput.on("focusout", () => {
            if (!this.titleInput.val()) {
                this.titleInput.val(this.data["title"])
            }
        })
    }

    createTopDragTarget() {
        let dragTarget = $(`<div class='editable-drag-target' data-location="0"></div>`)
        this.parentDiv.append(dragTarget)
        dragTarget.droppable({
            activeClass: 'editable-drag-active',
            hoverClass: 'editable-drag-hover',
            drop: (event, ui) => {
                let location = parseInt(dragTarget.data("location"))
                let draggable_id = ui.draggable[0].id
                let is_block_adder = $(ui.draggable[0]).data("block-adder") === ""
                if (is_block_adder) this.createBlock(dragTarget, draggable_id, location)
            }
        })
    }

    createBlock(preceding_element, block_type, location) {
        // let preceding_element = this.parentDiv.children().eq(parseInt(location))
        if (block_type === "addBlockText") {
            let block = new EditableTextBlock(this)
            this.data["blocks"].splice(location, 0, block)
            block.insert_after(preceding_element)
            block.create_droppable()
        }
        // preceding_element.after($(`<h3 style="background-color: red;">Test</h3>`))
    }

    generateBlockName() {
        let i = 0;
        let name = "A"
        while (!this.isValidBlockName(name)) {
            i++
            name = generateName(i)
        }
        return name
    }

    isValidBlockName(name) {
        if (!name) return false
        for (let i=0; i<this.data["blocks"].length; i++) {
            if (this.data["blocks"][i].name === name) {
                return false
            }
        }
        return true
    }

    get_json() {
        let json = {
            title: this.data["title"],
            author: this.data["author"],
            blocks: []
        }
        for (let i=0; i<this.data["blocks"].length; i++) {
            let block = this.data["blocks"][i]
            json.blocks.push(block.get_json())
        }
        return json
    }
}


class EditableBlock {
    constructor(editableCodePage, createBasics=true) {
        this.editableCodePage = editableCodePage
        this.name = this.editableCodePage.generateBlockName()
        this.editableCodePage.data

        if (createBasics) {
            this.blockDiv = $(`
                <div>
                    <div class="editable-block-header input-group" data-children-count="1">
                        <div class="btn shadow-none editable-block-name-button bg-extra-light text-dark pe-0 h3 m-0 text-white">Text Block:</div>
                        <input type='text' style='flex:1 1 auto;' class='bg-extra-light m-0 editable-block-name-input' placeholder='Block Name' value='${this.name}'>
                        <button class="btn editable-block-button"><span class="fas fa-chevron-up"></span></button>
                        <button class="btn editable-block-button"><span class="fas fa-chevron-down"></span></button>
                        <button class="btn editable-block-button"><span class="fas fa-trash-alt"></span></button>
                    </div>
                </div>`)
            this.nameInput = this.blockDiv.children().eq(0).children().eq(1)
            this.nameInput.on("keyup", () => {
                let new_name = this.nameInput.val()
                if (this.editableCodePage.isValidBlockName(new_name)) {
                    this.name = new_name
                }
            })
            this.nameInput.on("focusout", () => {
                let new_name = this.nameInput.val()
                if (!this.editableCodePage.isValidBlockName(new_name)) {
                    this.nameInput.val(this.name)
                } else {
                    this.name = new_name
                }
            })
        }

    }

    insert_after(preceding_element) {
        preceding_element.after(this.blockDiv)
    }

    create_droppable() {
        let dragTarget = $(`<div class='editable-drag-target' data-location="${this.get_position()+1}"></div>`)
        this.blockDiv.after(dragTarget)
        dragTarget.droppable({
            activeClass: 'editable-drag-active',
            hoverClass: 'editable-drag-hover',
            drop: (event, ui) => {
                let location = parseInt(dragTarget.data("location"))
                let draggable_id = ui.draggable[0].id
                let is_block_adder = $(ui.draggable[0]).data("block-adder") === ""
                if (is_block_adder) this.editableCodePage.createBlock(dragTarget, draggable_id, location)
            }
        })
        return dragTarget
    }

    get_position() {
        for (let i=0; i<this.editableCodePage.data["blocks"].length; i++) {
            if (this.editableCodePage.data["blocks"][i]) {
                return i
            }
        }
        throw new Error("Could not find this block in CodePage data.")
    }

    get_json() {
        return {}
    }
}


class EditableTextBlock extends EditableBlock {
    constructor(editableCodePage) {
        super(editableCodePage, true);
        this.textarea = $(`<textarea data-block="${this.name}" data-type="text-body" class="editable-block-textarea bg-light" placeholder="Edit this text"></textarea>`)
        this.blockDiv.append(this.textarea)
        this.text = ""

        this.textarea.on("keyup", () => {
            this.text = this.textarea.val()
        })
    }

    get_json() {
        return {
            name: this.name,
            text: this.text
        }
    }
}