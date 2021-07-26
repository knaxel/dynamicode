
function load_editable_codepage(parentDivId, json_data) {
    let editableCodepage = new EditableCodePage(parentDivId, json_data)
    if (json_data["blocks"].length === 0) {
        editableCodepage.createTopDragTarget()
    }

    let draggables = $("a[data-block-adder]")
    draggables.draggable({
        revert: true,
        revertDuration: 0,
        cursorAt: {left: 60, top: 60},
        start: () => {
            editableCodepage.windowMouseMove = $(window).on('mousemove', e => {
                editableCodepage.checkDragTargets(e.pageY, e.pageX)
            });
        },
        stop: () => {
            editableCodepage.stopDragging()
            editableCodepage.windowMouseMove.unbind()
        }
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


function mouseWithinTarget(top, left, target) {
    let offset = target.offset()
    let targetTop = offset.top;
    let targetBottom = offset.top + target.height();
    let targetLeft = offset.left;
    let targetRight = offset.left + target.width();

    return (targetTop <= top && top <= targetBottom) && (targetLeft <= left && left <= targetRight)
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
        this.titleInput.on("keyup", () => {
            if (this.titleInput.val()) {
                this.data["title"] = this.titleInput.val()
            }
        })
        this.titleInput.on("focusout", () => {
            if (!this.titleInput.val()) {
                this.titleInput.val(this.data["title"])
            }
        })

        this.droppable = undefined
    }

    createTopDragTarget() {
        let dragTarget = $(`<div class='editable-drag-target' data-location="0"></div>`)
        this.parentDiv.append(dragTarget)
        dragTarget.droppable({
            activeClass: 'editable-drag-active',
            // hoverClass: 'editable-drag-hover',
            drop: (event, ui) => {
                let location = parseInt(dragTarget.data("location"))
                let draggable_id = ui.draggable[0].id
                let is_block_adder = $(ui.draggable[0]).data("block-adder") === ""
                if (is_block_adder) this.createBlock(dragTarget, draggable_id, location)
            }
        })

        this.droppable = dragTarget
    }

    checkDragTargets(top, left) {
        if (mouseWithinTarget(top, left, this.droppable)) {
            this.droppable.addClass("editable-drag-hover")
        } else {
            this.droppable.removeClass("editable-drag-hover")
            for (let i=0; i<this.data.blocks.length; i++) {
                this.data.blocks[i].checkDragTarget(top, left)
            }
        }
    }

    stopDragging() {
        this.droppable.removeClass("editable-drag-hover")
        for (let i=0; i<this.data.blocks.length; i++) {
            this.data.blocks[i].stopDragging()
        }
    }

    createBlock(preceding_element, block_type, location) {
        // let preceding_element = this.parentDiv.children().eq(parseInt(location))
        if (block_type === "addBlockText") {
            let block = new EditableTextBlock(this)
            this.data["blocks"].splice(location, 0, block)
            block.insert_after(preceding_element)
            block.create_droppable()
        } else if (block_type === "addBlockCode") {
            let block = new EditableCodeBlock(this)
            this.data["blocks"].splice(location, 0, block)
            block.insert_after(preceding_element)
            block.create_droppable()
        } else if (block_type === "addBlockChoice") {
            let block = new EditableChoiceBlock(this)
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
    constructor(editableCodePage, type, header_style="editable-header-light") {
        this.editableCodePage = editableCodePage
        this.name = this.editableCodePage.generateBlockName()
        this.type = type
        this.editableCodePage.data

        this.blockDiv = $(`
            <div class="mb-0">
                <div class="input-group" data-children-count="1">
                    <div class="shadow-none editable-block-name text-dark pe-0 m-0 pt-1 pb-1 text-white ${header_style}"><span class="editable-block-name">${type} Block:</span></div>
                    <input type='text' style='flex:1 1 auto;' class='m-0 editable-block-name-input pt-1 pb-1 ${header_style}' placeholder='Block Name' value='${this.name}'>
                    <button class="editable-block-button pt-1 pb-1 ${header_style}"><span class="fas fa-chevron-up"></span></button>
                    <button class="editable-block-button pt-1 pb-1 ${header_style}"><span class="fas fa-chevron-down"></span></button>
                    <button class="editable-block-button editable-end-button pt-1 pb-1 pr-2 ${header_style}"><span class="fas fa-trash-alt"></span></button>
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

        this.setup_buttons()

        this.droppable = undefined
        this.highlightTimeout = undefined
    }

    insert_after(preceding_element) {
        preceding_element.after(this.blockDiv)
    }

    create_droppable() {
        let dragTarget = $(`<div class='editable-drag-target' data-location="${this.get_position()+1}"></div>`)
        this.blockDiv.after(dragTarget)
        dragTarget.droppable({
            activeClass: 'editable-drag-active',
            // hoverClass: 'editable-drag-hover',
            drop: (event, ui) => {
                let location = parseInt(dragTarget.data("location"))
                let draggable_id = ui.draggable[0].id
                let is_block_adder = $(ui.draggable[0]).data("block-adder") === ""
                if (is_block_adder) this.editableCodePage.createBlock(dragTarget, draggable_id, location)
            }
        })
        this.droppable = dragTarget
        return dragTarget
    }

    checkDragTarget(top, left) {
        if (mouseWithinTarget(top, left, this.droppable)) {
            this.droppable.addClass("editable-drag-hover")
        } else {
            this.droppable.removeClass("editable-drag-hover")
        }
    }

    stopDragging() {
        this.droppable.removeClass("editable-drag-hover")
    }

    setup_buttons() {
        let header_div = this.blockDiv.children().eq(0).children()
        let up_button = header_div.eq(2)
        let down_button = header_div.eq(3)
        let trash_button = header_div.eq(4)

        up_button.click(() => {
            this.move(-1)
            setTimeout(() => {up_button.blur()}, 200)
        })
        down_button.click(() => {
            this.move(1)
            setTimeout(() => {down_button.blur()}, 200)
        })

        trash_button.click(() => {
            let delete_button = $("#deleteBlockButton")
            $("#deleteBlockModal").modal("show")
            delete_button.off("click")
            delete_button.click(() => {
                this.delete()
            })
            $("#deleteBlockName").text(this.name)
        })
    }

    delete() {
        let position = this.get_position()
        this.editableCodePage.data["blocks"].splice(position, 1)
        this.blockDiv.remove()
        this.droppable.remove()
    }

    move(direction) {
        let position = this.get_position()
        if (direction !== -1 && direction !== 1) return
        if (direction === -1 && position === 0) return
        if (direction === 1 && position === this.editableCodePage.data["blocks"].length - 1) return

        let new_position = position + direction
        this.editableCodePage.data["blocks"].splice(position, 1)
        let preceding_element = this.editableCodePage.droppable
        if (new_position > 0) {
            preceding_element = this.editableCodePage.data["blocks"][new_position-1].droppable
        }

        this.editableCodePage.data["blocks"].splice(new_position, 0, this)
        this.blockDiv.detach()
        this.droppable.detach()

        preceding_element.after(this.blockDiv)
        this.blockDiv.after(this.droppable)
    }


    get_position() {
        for (let i=0; i<this.editableCodePage.data["blocks"].length; i++) {
            if (this.editableCodePage.data["blocks"][i].name === this.name) {
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
        super(editableCodePage, "Text")
        this.textarea = $(`<textarea class="editable-block-textarea bg-light" placeholder="Edit this text"></textarea>`)
        this.blockDiv.append(this.textarea)
        this.text = ""

        this.textarea.on("keyup", () => {
            this.text = this.textarea.val()
        })
    }

    get_json() {
        return {
            name: this.name,
            text: this.text,
            type: "TextBlock"
        }
    }
}


class EditableChoiceBlock extends EditableBlock {
    constructor(editableCodePage) {
        super(editableCodePage, "Choice")
        this.textarea = $(`<textarea class="editable-block-textarea--border-0 bg-light" placeholder="Edit this text"></textarea>`)
        this.blockDiv.append(this.textarea)
        this.text = ""
        this.choices = []

        this.textarea.on("keyup", () => {
            this.text = this.textarea.val()
        })

        let choiceContainer = $(`<div class="editable-block-choice-container"><div>Choices:</div></div>`)
        this.choiceDiv = $(`<div></div>`)
        let addChoiceDiv = $(`<div></div>`)
        choiceContainer.append(this.choiceDiv)
        choiceContainer.append(addChoiceDiv)

        this.addButton = $(`<button class='btn shadow-sm rounded-5 editable-choice-minus text-white fas fa-plus' type='button'></button>`)
        addChoiceDiv.append(this.addButton)
        this.addButton.on("click", () => {this.add_choice()})

        this.blockDiv.append(choiceContainer)

        this.add_choice()
    }

    add_choice() {
        let index = this.choices.length
        let choice = new Choice(this, this.choiceDiv, index)
        this.choices.push(choice)
    }

    removeChoice(index) {
        this.choices[index].remove()
        this.choices.splice(index, 1)
        for (let i=0; i<this.choices.length; i++) {
            this.choices[i].set_index(i)
        }
        if (this.choices.length === 0) {
            this.add_choice()
        }
    }

    get_json() {
        let data = {
            name: this.name,
            text: this.text,
            choices: [],
            type: "ChoiceBlock"
        }

        for (let i=0; i<this.choices.length; i++) {
            data.choices.push(this.choices[i].text)
        }

        return data
    }
}


class Choice {
    constructor(choiceBlock, choiceDiv, index) {
        this.choiceBlock = choiceBlock
        this.choiceDiv = choiceDiv
        this.index = index
        this.text = ""

        this.choice = $(`
            <div class='rounded-5 input-group p-0 mb-2 shadow-sm' data-children-count='1'>
                <button class='btn shadow-none rounded-5 bg-extra-light pe-2 m-0 text-white' type='button'><b>${this.index+1}</b></button>
            </div>"`)
        this.indexLabel = this.choice.children().eq(0).children().eq(0)

        this.input = $(`<input type='text' style='flex:1 1 auto;' class='border-0 bg-dark rounded-5 m-0 ps-3 p-1' placeholder='Choice text' value=''>`)
        this.choice.append(this.input)

        this.remove_button = $(`<button class='btn shadow-none rounded-5 editable-choice-minus pe-3 m-0 text-white fas fa-minus' type='button'></button>`)
        this.choice.append(this.remove_button)

        this.remove_button.on("click", () => {
            this.choiceBlock.removeChoice(this.index)
        })
        this.input.on("keyup", () => {
            this.text = this.input.val()
        })

        this.choiceDiv.append(this.choice)
    }

    set_index(new_index) {
        this.index = new_index
        this.indexLabel.text((new_index + 1).toString())
    }

    remove() {
        this.choice.remove()
    }
}


class EditableCodeBlock extends EditableBlock {
    constructor(editableCodePage) {
        super(editableCodePage, "Code", "editable-header-code")
        this.codeDiv = $(`<div></div>`)
        this.blockDiv.append(this.codeDiv)
        this.codeDiv.after(`<div class="editable-code-end d-flex justify-content-around">
<div class="editable-code-end--bar"></div><div class="editable-code-end--block"></div>
</div>`)
        this.large = false
        this.create_resize_button()

        setTimeout(() => {
            this.codeEditor = createCodeBlock(this.codeDiv[0])
            this.codeEditor.setSize(null, 150)
        }, 100)
    }

    create_resize_button() {
        let button = $(`<button class="editable-block-button pt-1 pb-1 editable-header-code"></button>`)
        let span = $(`<span class="fas fa-expand-arrows-alt"></span>`)
        button.append(span)
        button.on("click", () => {
            if (this.large) {
                this.large = false
                this.codeEditor.setSize(null, 150)
                span.removeClass("fa-compress-arrows-alt")
                span.addClass("fa-expand-arrows-alt")
            } else {
                this.large = true
                this.codeEditor.setSize(null, 500)
                span.removeClass("fa-expand-arrows-alt")
                span.addClass("fa-compress-arrows-alt")
            }
        })
        this.blockDiv.children().eq(0).children().eq(1).after(button)
    }

    get_json() {
        return {
            name: this.name,
            code: this.codeEditor.doc.getValue(),
            type: "CodeBlock"
        }
    }
}