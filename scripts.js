document.addEventListener('DOMContentLoaded', function () {
    var modal = document.getElementById('modal');
    var closeModalBtns = document.getElementsByClassName('close');
  
    for (var i = 0; i < closeModalBtns.length; i++) {
      closeModalBtns[i].onclick = function () {
        modal.style.display = 'none';
      };
    }

  });
function btnclick(id){
    var replybox = document.getElementById('reply-box');
    replybox.src = "res/" + id + ".html"
    modal.style.display = 'block';
}