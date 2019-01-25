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


  // Show customer detail info edit box
  $('#page-container').on('click', '.info-row', function(){
    $(this).children('.info-view').addClass('is-hidden');
    $(this).children('.info-input').removeClass('is-hidden');
  });


  // Hide customer detail info edit box
  $('#page-container').on('click', '.detail-form-cancel', function(){
    $(this).closest('.info-row').children('.info-view').removeClass('is-hidden');
    $(this).closest('.info-input').addClass('is-hidden');
    return false;
  });


  // Submit customer detail info edit box
  $('#page-container').on('submit', '.detail-form', function(){
    var form = $(this);
    var pk = form.attr('data-pk');

    $.ajax({
      url: '/customers/' + pk + '/update',
      data: form.serialize(),
      type: 'post',
      dataType: 'json',
      success: function(data){
        if (data.result == 'ok') {
          var value = "";
          if (form.attr('data-name') == "address") {
            var address1 = form.find('.input[name=address1]').val();
            var address2 = form.find('.input[name=address2]').val();
            value = address1 + " " + address2;
          }
          else {
            value = form.find('.input').val();
          }

          var info_row = form.closest('.info-row');
          info_row.find('.info-value').text(value);
          info_row.children('.info-view').removeClass('is-hidden');
          info_row.children('.info-input').addClass('is-hidden');
        }
        else {
          console.log(data.error);
        }
      }
    });

    return false;
  });

});
