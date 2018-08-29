function addToCart(good_id) {
    // var csrf = $('input[name="csrfmiddlewaretoken"]').val
    $.ajax({
        url:'/home/add_to_cart/',
        type: 'POST',
        dataType:'json',
        // headers:{'X-CSREToken': csrf},
        data:{'good_id': good_id},
        success:function(data){
            money()
            console.log(data.data.c_num)
            $('#num_'+good_id).html(data.data.c_num)
        },
        error:function(data){
            alert('请登录')
        }
    })
}


function minusToCart(good_id) {
    $.ajax({
        url:'/home/minus_to_cart/',
        type: 'POST',
        dataType:'json',
        data:{'good_id': good_id},
        success:function(data){
           money()
            console.log(data.data.c_num)
            $('#num_'+good_id).html(data.data.c_num)
            if (data.data.c_num == '0' ){
                $('#cartnum_'+good_id).remove()
                }
        },
        error:function(data){
            alert('请登录')
        }
    })
}

//
$.get('/home/refresh_goods/',function(data){
     money()
    if (data.code == '200'){
        for(var i=0; i<data.data.length;i++)
            $('#num_'+ data.data[i][0]).html(data.data[i][1])
    }
})


//单选
function select1(good_id){
    $.post('/home/delselect/',{'good_id':good_id},function (data) {
         money()
        if (data.code == '200'){
            if(data.is_select){
                $('#select'+good_id).html('√')
                if(data.all){
                    $('#total').html('√')
                }
            }
            else{
                $('#select'+good_id).html('')
                $('#total').html('')
            }
        }
    })
}


//全选
function select2() {

    $.get('/home/allselect/',function(data){

    money()
        if(data.all){
              $('#total').html('√')
            for (var i = 0 ; i < data.goods_id.length ; i++){
                  $('#select'+data.goods_id[i]).html('√')

            }
        }
        else{
             $('#total').html('')
              for (var i = 0 ; i < data.goods_id.length ; i++){
                    $('#select'+data.goods_id[i]).html('')
            }
        }
    })
}


//钱
function money(){
    $.get('/home/money/',function(data){
        $('#allmoney').html('总价:'+data.money)
    })
}


money()