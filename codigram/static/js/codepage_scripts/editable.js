
function load_editable_codepage(parentDivId, json_data) {
    let editableCodepage = new EditableCodePage(parentDivId, json_data)
    editableCodepage.createTopDragTarget()
    editableCodepage.load_blocks(json_data)

    let draggables = $("a[data-block-adder]")
    draggables.draggable({
        revert: true,
        revertDuration: 0,
        cursorAt: {left: 60, top: 20},
        start: (event, ui) => {
            editableCodepage.windowMouseMove = $(window).on('mousemove', e => {
                editableCodepage.checkDragTargets(e.pageY, e.pageX)
            });
        },
        stop: () => {
            editableCodepage.stopDragging()
            editableCodepage.windowMouseMove.unbind()
        }
    })
    $(window).resize(() => {setDraggablesOffset(draggables)})
    setDraggablesOffset(draggables)
    setupControlButtons(parentDivId, editableCodepage)
    return editableCodepage
}


function setDraggablesOffset(draggables) {
    draggables.draggable("option", "cursorAt", {
        left: Math.floor(draggables.width()/2),
        top: Math.floor(draggables.height()/2)
    })
}


function generateName(i) {
    let alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if (i < 26) {
        return alphabet[i]
    }
    return generateName(Math.floor(i/26)-1) + alphabet[i%26]
}


function htmlUnsafe(safe_string) {
    return String(safe_string).replace(/&amp;/g, '&').replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>').replace(/&quot;/g, '"')
        .replace(/&#34;/g, '"').replace(/&#39;/g, "'");
}


function mouseWithinTarget(top, left, target) {
    let offset = target.offset()
    let targetTop = offset.top;
    let targetBottom = offset.top + target.height();
    let targetLeft = offset.left;
    let targetRight = offset.left + target.width();

    return (targetTop <= top && top <= targetBottom) && (targetLeft <= left && left <= targetRight)
}


function setupControlButtons(editCodePageId, editableCodePage) {
    let modeButton = $("#toggleModeButton")
    let reorderButton = $("#reorderButton")
    let editMenu = $("#editMenu")
    let editCodePage = $(`#${editCodePageId}`)

    modeButton.click(() => {
        if (modeButton.text() === "Switch to View Mode") {
            modeButton.text("Switch to Edit Mode")
            editCodePage.after("<div id='viewCodePage' class='col-lg mt-4 mb-5'></div>")
            load_codepage("viewCodePage", editableCodePage.get_json())
            editCodePage.hide()
            reorderButton.hide()
            editMenu.hide()
        } else {
            modeButton.text("Switch to View Mode")
            reset_skulpt_instances()
            $("#viewCodePage").remove()
            editCodePage.show()
            reorderButton.show()
            editMenu.show()
        }
    })
}


function save(save_button, post_button, status_elem, saveURL, editableCodePage, callback=null) {
    save_button.attr("disabled", true)
    post_button.attr("disabled", true)
    status_elem.text("Saving...")

    $.ajax({
            url: saveURL,
            type: "POST",
            data: JSON.stringify(editableCodePage.get_json()),
            contentType: "application/json",
            dataType: "json",
            success: null
        }).done((data) => {
            if (data.success) {
                status_elem.text("Saved!")
                if (callback) {
                    callback(data)
                }
            } else {
                console.log(data.message)
                status_elem.text("Failed to save")
            }
        }).fail(() => {
            status_elem.text("Failed to save")
        }).always(() => {
            save_button.attr("disabled", false)
            post_button.attr("disabled", false)
            setTimeout(() => {
                status_elem.text("")
            }, 2000)
        })
}


function setupSaveButtons(editableCodePage, saveURL, saveButtonId, statusId, postURL=null, viewURL=null, postButtonId=null, replaceViewUUID=false) {
    let save_button = $(`#${saveButtonId}`)
    let post_button = $(`#${postButtonId}`)
    let status_elem = $(`#${statusId}`)

    save_button.click(() => {
        save(save_button, post_button, status_elem, saveURL, editableCodePage)
    })

    post_button.click(() => {
        save(save_button, post_button, status_elem, postURL, editableCodePage, (data) => {
            if (replaceViewUUID) {
                viewURL = viewURL.replace("YYY", data.codepage_uuid)
            }
            window.location = viewURL;
        })
    })
}


class EditableCodePage {
    constructor(parentDivId, json_data) {
        this.parentDivId = parentDivId
        this.parentDiv = $(`#${parentDivId}`)
        this.data = {
            title: json_data.title, author: json_data.author,
            date_created: json_data.date_created, blocks: [],
            date_edited: json_data.date_edited,
            codepage_uuid: json_data.codepage_uuid,
            author_uuid: json_data.author_uuid
        }

        this.titleDiv = $(`
            <div class='rounded-5 input-group p-0 shadow-sm mb-3' data-children-count='1'>
            <button class='btn shadow-none rounded-5 bg-extra-light text-dark pe-2 h3 m-0 text-white' type='button'>Title</button>
            <input id='editableTitle' type='text' style='flex:1 1 auto;' class='h3 border-0 bg-light rounded-5 m-0 ps-3 p-1' placeholder='Title' value='${this.data["title"]}'>
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

    load_blocks(json_data) {
        let preceding_element = this.droppable
        for (let i=0; i<json_data.blocks.length; i++) {
            let block_data = json_data.blocks[i]
            let new_block = this.createBlock(preceding_element, block_data.type, i, block_data)
            preceding_element = new_block.droppable
        }
    }

    createTopDragTarget() {
        let dragTarget = $(`<div class='editable-drag-target' data-location="0"></div>`)
        this.parentDiv.append(dragTarget)
        dragTarget.droppable({
            activeClass: 'editable-drag-active',
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

    createBlock(preceding_element, block_type, location, data) {
        if (block_type === "addBlockText" || block_type === "TextBlock") {
            let block = new EditableTextBlock(this, data)
            this.data["blocks"].splice(location, 0, block)
            block.insert_after(preceding_element)
            block.create_droppable()
            return block
        } else if (block_type === "addBlockCode" || block_type === "CodeBlock") {
            let block = new EditableCodeBlock(this, data)
            this.data["blocks"].splice(location, 0, block)
            block.insert_after(preceding_element)
            block.create_droppable()
            return block
        } else if (block_type === "addBlockChoice" || block_type === "ChoiceBlock") {
            let block = new EditableChoiceBlock(this, data)
            this.data["blocks"].splice(location, 0, block)
            block.insert_after(preceding_element)
            block.create_droppable()
            return block
        } else if (block_type === "addBlockImage" || block_type === "ImageBlock") {
            let block = new EditableImageBlock(this, data)
            this.data["blocks"].splice(location, 0, block)
            block.insert_after(preceding_element)
            block.create_droppable()
            return block
        } else if (block_type === "addBlockSlider" || block_type === "SliderBlock") {
            let block = new EditableSliderBlock(this, data)
            this.data["blocks"].splice(location, 0, block)
            block.insert_after(preceding_element)
            block.create_droppable()
            return block
        }
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
            author_uuid: this.data["author_uuid"],
            codepage_uuid: this.data["codepage_uuid"],
            date_created: this.data["date_created"],
            date_edited: this.data["date_edited"],
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
    constructor(editableCodePage, data, type, header_style="editable-header-light") {
        this.editableCodePage = editableCodePage
        if (data && data.name) {
            this.name = data.name
        } else {
            this.name = this.editableCodePage.generateBlockName()
        }
        this.type = type
        this.editableCodePage.data

        this.blockDiv = $(`
            <div class="mb-0">
                <div class="input-group" data-children-count="1">
                    <div class="shadow-none editable-block-name text-dark pe-0 m-0 pt-1 pb-1 text-white ${header_style}"><span class="editable-block-name">${type} Block:</span></div>
                    <input type='text' style='flex:1 1 auto;' class='m-0 editable-block-name-input pt-1 pb-1 ${header_style}' placeholder='Block Name' value='${htmlUnsafe(this.name)}'>
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
    constructor(editableCodePage, data) {
        super(editableCodePage, data, "Text")
        this.textarea = $(`<textarea class="editable-block-textarea bg-light" placeholder="Edit this text"></textarea>`)
        this.blockDiv.append(this.textarea)
        this.text = ""
        if (data && data.text) this.text = data.text

        this.textarea.val(htmlUnsafe(this.text))
        this.textarea.on("keyup", () => {
            this.text = this.textarea.val()
        })
    }

    get_json() {
        return {
            name: htmlUnsafe(this.name),
            text: htmlUnsafe(this.text),
            type: "TextBlock"
        }
    }
}

class EditableChoiceBlock extends EditableBlock {
    constructor(editableCodePage, data) {
        super(editableCodePage, data, "Choice")
        this.textarea = $(`<textarea class="editable-block-textarea--border-0 bg-light" placeholder="Edit this text"></textarea>`)
        this.blockDiv.append(this.textarea)
        this.text = ""
        if (data && data.text) {this.text = data.text}
        this.choices = []

        this.textarea.val(htmlUnsafe(this.text))
        this.textarea.on("keyup", () => {
            this.text = this.textarea.val()
        })

        let choiceContainer = $(`<div class="editable-block-bottom-container"><div>Choices:</div></div>`)
        this.choiceDiv = $(`<div></div>`)
        let addChoiceDiv = $(`<div></div>`)
        choiceContainer.append(this.choiceDiv)
        choiceContainer.append(addChoiceDiv)

        this.addButton = $(`<button class='btn shadow-sm rounded-5 editable-choice-plus text-white fas fa-plus' type='button'></button>`)
        addChoiceDiv.append(this.addButton)
        this.addButton.on("click", () => {this.add_choice()})

        this.blockDiv.append(choiceContainer)

        if (data && data.choices) {
            for (let i=0; i<data.choices.length; i++) {
                this.add_choice(data.choices[i])
            }
        } else {
            this.add_choice()
        }
    }

    add_choice(choice_text) {
        let index = this.choices.length
        let choice = new Choice(this, this.choiceDiv, index, choice_text)
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
            name: htmlUnsafe(this.name),
            text: htmlUnsafe(this.text),
            choices: [],
            type: "ChoiceBlock"
        }

        for (let i=0; i<this.choices.length; i++) {
            data.choices.push(htmlUnsafe(this.choices[i].text))
        }

        return data
    }
}


class Choice {
    constructor(choiceBlock, choiceDiv, index, text="") {
        this.choiceBlock = choiceBlock
        this.choiceDiv = choiceDiv
        this.index = index
        this.text = text

        this.choice = $(`
            <div class='rounded-5 input-group p-0 mb-2 shadow-sm' data-children-count='1'>
                <button class='btn shadow-none rounded-5 bg-extra-light pe-2 m-0 text-white' type='button'><b>${this.index+1}</b></button>
            </div>"`)
        this.indexLabel = this.choice.children().eq(0).children().eq(0)

        this.input = $(`<input type='text' style='flex:1 1 auto;' class='border-0 bg-dark rounded-5 m-0 ps-3 p-1' placeholder='Choice text' value=''>`)
        this.choice.append(this.input)

        this.remove_button = $(`<button class='btn shadow-none rounded-5 editable-choice-minus pe-3 m-0 text-white fas fa-minus' type='button'></button>`)
        this.choice.append(this.remove_button)

        this.input.val(htmlUnsafe(this.text))
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
    constructor(editableCodePage, data) {
        super(editableCodePage, data, "Code", "editable-header-code")
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
            if (data && data.code) this.codeEditor.doc.setValue(data.code)
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
            name: htmlUnsafe(this.name),
            code: this.codeEditor.doc.getValue(),
            type: "CodeBlock"
        }
    }
}


class EditableImageBlock extends EditableBlock {
    constructor(editableCodePage, data) {
        super(editableCodePage, data, "Image")
        this.textarea = $(`<textarea class="editable-block-textarea--border-0 bg-light" placeholder="Edit this text"></textarea>`)

        let imgContainer = $(`<div class="editable-block-bottom-container"></div>`)
        let imgSource = $(`<div class='rounded-5 input-group p-0 mb-2 shadow-sm' data-children-count='1'></div>"`)
        this.input = $(`<input type='text' style='flex:1 1 auto;' class='border-0 bg-dark rounded-5 m-0 ps-3 p-1' placeholder='Image Source URL' value=''>`)
        this.updateButton = $(`<button class='btn shadow-none rounded-5 editable-choice-minus pe-3 m-0 text-white' type='button'>Update</button>`)

        imgContainer.append(imgSource)
        imgSource.append(this.input)
        imgSource.append(this.updateButton)

        this.img = $('<img class="img-responsive d-block mx-auto" width="300" src="" alt=""/>')

        this.blockDiv.append(this.textarea)

        this.blockDiv.append(imgContainer)
        imgContainer.append(this.img)

        this.text = ""
        this.src = ""
        if (data && data.text) this.text = data.text
        if (data && data.src) this.set_src(data.src)

        this.textarea.val(htmlUnsafe(this.text))
        this.input.val(htmlUnsafe(this.src))
        this.textarea.on("keyup", () => {
            this.text = this.textarea.val()
        })
        this.updateButton.on("click", () => {
            this.set_src(this.input.val())
        })
        this.img.hide()
    }

    set_src(src) {
        this.src = src
        this.img.attr("src", src + "?t="+ new Date().getTime());
    }

    get_json() {
        return {
            name: htmlUnsafe(this.name),
            text: htmlUnsafe(this.text),
            src: htmlUnsafe(this.src),
            type: "ImageBlock"
        }
    }
}


class EditableSliderBlock extends EditableBlock {
    constructor(editableCodePage, data) {
        super(editableCodePage, data, "Slider")
        this.textarea = $(`<textarea class="editable-block-textarea--border-0 bg-light" style="min-height:50px" placeholder="Edit this text"></textarea>`)
        this.blockDiv.append(this.textarea)

        let bottomContainer = $(`<div class="editable-block-bottom-container"></div>`)

        let lowerBoundContainer = $(`
            <div class='rounded-5 input-group p-0 mb-2' data-children-count='1'>
                <button class='btn shadow-none rounded-5 bg-extra-light pe-2 m-0 text-white' style="width: 5em;" type='button'>Lower</button>
            </div>"`)
        this.lowerBoundInput = $(`<input type='number' style='flex:1 1 auto;' class='border-0 bg-dark rounded-5 m-0 ps-3' placeholder='Lower Bound' value='0'>`)
        lowerBoundContainer.append(this.lowerBoundInput)

        let upperBoundContainer = $(`
            <div class='rounded-5 input-group p-0 mb-2' data-children-count='1'>
                <button class='btn shadow-none rounded-5 bg-extra-light pe-2 m-0 text-white' style="width: 5em;" type='button'>Upper</button>
            </div>"`)
        this.upperBoundInput = $(`<input type='number' style='flex:1 1 auto;' class='border-0 bg-dark rounded-5 m-0 ps-3' placeholder='Lower Bound' value='100'>`)
        upperBoundContainer.append(this.upperBoundInput)

        let defaultValueContainer = $(`
            <div class='rounded-5 input-group p-0 mb-2' data-children-count='1'>
                <button class='btn shadow-none rounded-5 bg-extra-light pe-2 m-0 text-white' style="width: 5em;" type='button'>Default</button>
            </div>"`)
        this.defaultValueInput = $(`<input type='number' style='flex:1 1 auto;' class='border-0 bg-dark rounded-5 m-0 ps-3' placeholder='Lower Bound' value='50'>`)
        defaultValueContainer.append(this.defaultValueInput)

        bottomContainer.append(lowerBoundContainer)
        bottomContainer.append(upperBoundContainer)
        bottomContainer.append(defaultValueContainer)

        this.blockDiv.append(bottomContainer)

        this.text = ""
        this.lower = 0
        this.upper = 100
        this.default = 50
        if (data && data.text) this.text = data.text
        if (data && data.lower) this.lower = data.lower
        if (data && data.upper) this.upper = data.upper
        if (data && data.default) this.default = data.default

        this.textarea.val(htmlUnsafe(this.text))
        this.textarea.on("keyup", () => {
            this.text = this.textarea.val()
        })

        this.lowerBoundInput.val(this.lower)
        this.upperBoundInput.val(this.upper)
        this.defaultValueInput.val(this.default)
        this.lowerBoundInput.on("change", () => {this.update_slider_data()})
        this.upperBoundInput.on("change", () => {this.update_slider_data()})
        this.defaultValueInput.on("change", () => {this.update_slider_data()})
    }

    update_slider_data() {
        let lower = parseFloat(this.lowerBoundInput.val())
        let upper = parseFloat(this.upperBoundInput.val())
        let defaultValue = parseFloat(this.defaultValueInput.val())

        if (lower >= upper) {lower = upper - 1}
        if (defaultValue < lower) {defaultValue = lower}
        if (defaultValue > upper) {defaultValue = upper}

        this.lowerBoundInput.val(lower)
        this.upperBoundInput.val(upper)
        this.defaultValueInput.val(defaultValue)
    }

    get_json() {
        this.update_slider_data()
        return {
            name: htmlUnsafe(this.name),
            text: htmlUnsafe(this.text),
            lower: parseFloat(this.lowerBoundInput.val()),
            upper: parseFloat(this.upperBoundInput.val()),
            default: parseFloat(this.defaultValueInput.val()),
            type: "SliderBlock"
        }
    }
}