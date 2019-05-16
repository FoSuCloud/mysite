function likeChange(obj,content_type,object_id){
     var is_like=obj.getElementByClassName('active').length==0
     $.ajax({
        url:'{% url 'like_change' %}',
        type:'GET',
        data:{
           content_type:content_type,
           object_id:object_id,
           is_like:is_like,
        },
        cache:false,
        success:function(data){
            console.log(data)
        },
        error:function(xhr){
            console.log(xhr)
        }
     });
     }