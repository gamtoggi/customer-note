$(function(){

  // Show add customer form modal
  $('#customer-list-container').on('click', '#add-customer-btn', function(){
    $.ajax({
      url: '/customers/create',
      type: 'get',
      dataType: 'json',
      success: function(data){
        $('#form-container').html(data.html);
      }
    });
  });

  // Close add customer form modal
  $('#form-container').on('click', '#modal-cancel', function(){
    $('#form-modal').removeClass('is-active');
    return false;
  });

  // Submit add customer form
  $('#form-container').on('submit', '#add-customer-form', function(){
    var form = $(this);

    $.ajax({
      url: '/customers/create',
      data: form.serialize(),
      type: 'post',
      dataType: 'json',
      success: function(data){
        if (data.result == 'ok') {
          $('#customer-list-container').html(data.html);
          $('#form-modal').removeClass('is-active');
        }
        else {
          console.log(data.error);
        }
      }
    });

    return false;
  });

  // Show customer detail page
  $('#page-container').on('click', '.customer-list-item', function(){
    var pk = $(this).attr('data-customer-id');

    $.ajax({
      url: '/customers/' + pk,
      type: 'get',
      dataType: 'json',
      success: function(data){
        $('#page-container').html(data.html);
      }
    });

  });


  // Close customer detail page
  $('#page-container').on('click', '#detail-close-btn', function(){
    // var pk = $(this).attr('data-customer-id');

    $.ajax({
      url: '/customers/list',
      type: 'get',
      dataType: 'json',
      success: function(data){
        $('#page-container').html(data.html);
      }
    });

  });

});