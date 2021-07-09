
function load_post(divId, json_data) {
    let div = $(`#${divId}`)
    div.append(
        $(`<h2>${json_data["title"]}</h2>`)
    )
    div.append(
        $(`<p>${json_data["author"]}</p>`)
    )

    for (let i=0; i<json_data["blocks"].length; i++) {
        create_block_from_json(div, json_data["blocks"][i])
    }
    set_post_data(json_data)
}


function create_block_from_json(div, json_data) {
    let type = json_data["type"]
    let block = null;
    if (type === "TextBlock") {
        block = $(`<div class="post-block-container"><b>Block ${json_data["name"]}</b><div>${json_data["text"]}</div></div>`)
        div.append(block)

    } else if (type === "CodeBlock") {
        let name = json_data["name"]
        block = $(`<div class="post-code-block-container">${get_code_block(name)}</div>`)
        div.append(block)
        let code_runner = new CodeRunner(`codeEditor${name}`, `outputEditor${name}`,
            `inputBar${name}`, `runButton${name}`, `stopButton${name}`)
        set_resize_buttons(code_runner, `expandEditorButton${name}`,
            `shortenEditorButton${name}`, `expandConsoleButton${name}`,
            `shortenConsoleButton${name}`)
        code_runner.codeEditor.doc.setValue(json_data["code"])

    } else if (type === "ChoiceBlock") {
        block = $(`<div class="post-block-container"><b>Block ${json_data["name"]}</b><div>${json_data["text"]}</div>
<select class="form-control mt-2">
${render_options(json_data["choices"])}
</select>
</div>`)
        div.append(block)
    }

}


function get_code_block(name) {
    return `
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
    </div>`
}


function render_options(choices) {
    let options = ""

    for (let i=0; i<choices.length; i++) {
        let option = `<option value="${choices[i]}">${choices[i]}</option>`
        options = options + "\n" + option
    }

    return options
}

