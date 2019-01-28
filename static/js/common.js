function loadPartialPage(url, containerSelector) {
  $.ajax({
    url: url,
    type: 'get',
    dataType: 'json',
    success: function(data){
      $(containerSelector).html(data.html);
    }
  });
}


function findElement(self, selector) {
  if ($(selector).length > 0) {
    return $(selector);
  }
  if (self.children(selector).length > 0) {
    self.children(selector).html('');
  }
  else if (self.find(selector).length > 0) {
    self.find(selector).html('');
  }
  else if (self.closest(selector).length) {
    self.closest(selector).html('');
  }

  alert('Can not find ' + target);
  return null;
}

$(function(){

  // Navibar toggle
  $(".navbar-burger").click(function() {
      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      $(".navbar-burger").toggleClass("is-active");
      $(".navbar-menu").toggleClass("is-active");

  });



  /*
    <Partial 페이지 로드>
    class : js-partial-btn
    event : click
    attr : data-url (로드할 url)
          data-target (페이지를 붙일 element selector)
  */
  $('#page-container').on('click', '.js-partial-btn', function(){
    var url = $(this).attr('data-url');
    var target = $(this).attr('data-target');

    loadPartialPage(url, target);
  });


  /*
    <Element 보이기>
    class : js-show-btn
    event : click
    attr : data-target
  */
  $('#page-container').on('click', '.js-show-btn', function(){
    var target = findElement($(this), $(this).attr('data-target'));
    if (target != null) {
      target.removeClass('is-hidden');
    }
  });


  /*
    <Element 감추기>
    class : js-hide-btn
    event : click
    attr : data-target
  */
  $('#page-container').on('click', '.js-hide-btn', function(){
    var target = findElement($(this), $(this).attr('data-target'));
    if (target != null) {
      target.addClass('is-hidden');
    }
  });


  /*
    <Element 내용 없애기>
    class : js-clear-btn
    event : click
    attr : data-target
  */
  $('#page-container').on('click', '.js-clear-btn', function(){
    var target = findElement($(this), $(this).attr('data-target'));
    if (target != null) {
      target.html('');
    }
  });



  /*
    <checkbox toggle>
    class : js-toggle-checkbox
    event : change
    attr : data-target
  */
  $('#page-container').on('change', '.js-toggle-checkbox', function(){
    var target = findElement($(this), $(this).attr('data-target'));

    if (target != null) {
      var checked = $(this).is(':checked');
      
      if (checked) {
        target.removeClass('is-hidden');
      }
      else {
        target.addClass('is-hidden');
      }
    }
  });


  /*
    <Form 전송>
    class : js-form
    event : submit
    attr : action, method
  */
  $('#page-container').on('submit', '.js-form', function(){
    var form = $(this);
    $.ajax({
      url: form.attr('action'),
      data: form.serialize(),
      type: form.attr('method'),
      dataType: 'json',
      success: function(data){
        if (data.status == 200) {
          $('#page-container').html(data.html);
        }
        else {
          alert('죄송합니다. 데이터를 저장하지 못했습니다.');
          console.log(data.errors);
        }
      }
    });
    return false;
  });



  /*
    <정보 보여주다가 누르면 폼으로 바뀌는 박스>
    class : js-edit
    event : click
    children : js-info-container, js-form-container
  */
  $('#page-container').on('click', '.js-edit', function(){
    var self = $(this);
    if (self.children('.js-form-container').html().length == 0) {
      $.ajax({
        url: $(this).attr('data-url'),
        type: 'get',
        dataType: 'json',
        success: function(data){
          self.children('.js-info-container').addClass('is-hidden');
          self.children('.js-form-container').html(data.html);
        }
      });
    }
  });



  /*
    <정보 보여주다가 누르면 폼으로 바뀌었을 때 취소 누르면 폼 없애기>
    class : js-edit-cancel
    event : click
    position : js-edit 하위요소여야 한다.
  */
  $('#page-container').on('click', '.js-edit-cancel', function(){
    var root = $(this).closest('.js-edit');
    root.children('.js-info-container').removeClass('is-hidden');
    root.children('.js-form-container').html('');
    return false;
  });

});
