
function setup_quiz_controls(python_block) {
    let quiz_button = python_block.quiz_button
    let quiz_status_success = python_block.quiz_status_success
    let quiz_status_fail = python_block.quiz_status_fail

    quiz_button.click(() => {
        quiz_button.attr("disabled", true)
        quiz_button.popover("disable")
        let data = get_quiz_block_data(python_block)
        check_answer_with_server(data, quiz_button, quiz_status_success, quiz_status_fail)
    })
}


function check_answer_with_server(block_data, quiz_button, quiz_status_success, quiz_status_fail) {
    $.ajax({
        url: quizURL,
        type: "POST",
        data: JSON.stringify(block_data),
        contentType: "application/json",
        dataType: "json",
        success: null
    }).done((data) => {
        let timeout = 4000
        if (data.success) {
            quiz_button.attr("data-content", "Correct!")
            update_complete_labels(quiz_status_success, quiz_status_fail, data.module_completed)
            timeout = 2000
        } else {
            let text = "Incorrect."
            if (data.message) {text = text + " " + data.message}
            quiz_button.attr("data-content", text)
        }
        refresh_popover(quiz_button)
        close_popover(quiz_button, timeout)
    }).fail(() => {
        quiz_button.attr("data-content", "Failed to check answer.")
        refresh_popover(quiz_button)
        close_popover(quiz_button, 4000)
    })
}


function update_complete_labels(quiz_status_success, quiz_status_fail, module_completed) {
    quiz_status_fail.hide()
    quiz_status_success.show()
    if (module_completed) {
        markModuleAsComplete()
    }
}


function refresh_popover(button) {
    button.popover("enable")
    button.popover("hide")
    button.popover("show")
    button.popover("disable")
}


function close_popover(button, timeout) {
    setTimeout(() => {
        button.popover("hide")
        button.attr("data-content", "Checking...")
        button.popover("enable")
        button.attr("disabled", false)
    }, timeout)
}


function get_quiz_block_data(python_block) {
    let block_type = python_block.tp$name
    let name = python_block.$d.entries.name[1].v
    if (block_type === "TextBlock") {
        return {"block_type": block_type, "name": name, "text": python_block.text}
    } else if(block_type === "CodeBlock") {
        return {"block_type": block_type, "name": name, "text": python_block.text,
            "code": python_block.code_runner.codeEditor.doc.getValue(),
            "terminal": python_block.code_runner.terminalEditor.doc.getValue(),
            "scope": get_global_scope()}
    } else if(block_type === "ChoiceBlock") {
        return {"block_type": block_type, "name": name, "text": python_block.text,
            "value": python_block.select_div.val()}
    } else if(block_type === "ImageBlock") {
        return {"block_type": block_type, "name": name, "text": python_block.text,
            "src": python_block.img.prop("src")}
    } else if(block_type === "SliderBlock") {
        return {"block_type": block_type, "name": name, "text": python_block.text, "lower": python_block.lower,
            "upper": python_block.upper, "default": python_block.defaultValue, "value": python_block.value}
    }
    return {}
}


function get_global_scope() {
    let scope = {}
    for (let key in Sk.globals) {
        if (Sk.globals.hasOwnProperty(key) && Sk.globals[key].v) {
            scope[key] = Sk.globals[key].v
        }
    }
    return scope
}
