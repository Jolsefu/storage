function selectAll(source) {
    var checkboxes = document.querySelectorAll("input[type='checkbox']");
    for(var checkbox of checkboxes)
        checkbox.checked = source.checked;
}