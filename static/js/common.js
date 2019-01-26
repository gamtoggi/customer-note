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

$(function(){
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
    <Element 감추기>
    class : js-hide-btn
    event : click
    attr : data-target
  */
  $('#page-container').on('click', '.js-hide-btn', function(){
    var target = $(this).attr('data-target');

    if ($(this).children(target).length > 0) {
      $(this).children(target).addClass('is-hidden');
    }
    else if ($(this).find(target).length > 0) {
      $(this).find(target).addClass('is-hidden');
    }
    else if ($(this).closest(target).length) {
      $(this).closest(target).addClass('is-hidden');
    }
    else {
      alert('Can not find ' + target);
    }

    return false;
  });


  /*
    <Element 내용 없애기>
    class : js-clear-btn
    event : click
    attr : data-target
  */
  $('#page-container').on('click', '.js-clear-btn', function(){
    var target = $(this).attr('data-target');

    if ($(this).children(target).length > 0) {
      $(this).children(target).html('');
    }
    else if ($(this).find(target).length > 0) {
      $(this).find(target).html('');
    }
    else if ($(this).closest(target).length) {
      $(this).closest(target).html('');
    }
    else {
      alert('Can not find ' + target);
    }

    return false;
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