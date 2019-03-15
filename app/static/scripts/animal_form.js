// create custom file upload button and append to page in proper container
const button = document.createElement('button')
button.classList.add('btn')
button.classList.add('btn-outline-dark')
button.classList.add('btn-sm')
button.type = 'button'
button.textContent = 'Upload Image'
button.id = 'img_upload'
$('#div_id_image').find('div').append(button)

// hide the default file upload button and text
$('#div_id_image').find('div').find('input').hide()

// if editing, hide text in this label
$('#div_id_image').find('div').find('label').hide()

// make an element to hold the file name's text and append it to the page
div = document.createElement('div')
div.id = 'file_name_text'
$('#div_id_image').find('div').append(div)

// click function on custom button to trigger the default hidden file upload input
$('#img_upload').click(function(){
    $('#id_image').click()
})

// capture file name of selected image file
$(document).ready(function(){
$('input[type="file"]').change(function(e){
    // get file name
    fileName = e.target.files[0].name
    // calculate half the length of string (used for styling considerations)
    halfway = fileName.length / 2
    first_half = fileName.slice(0, halfway)
    second_half = fileName.slice(-halfway)
    // if the string is more than 16 chars, we need to reduce the length to 16ish chars before appending to page
    if (fileName.length > 16) {
        text = first_half.substring(0,7)+"..."+second_half.slice(-7)
        $('#div_id_image').find('div').find('#file_name_text').empty().append(text)
    } else {
        $('#div_id_image').find('div').find('#file_name_text').empty().append(fileName)
    }
})
})