$(document).ready(function(){
    $('.product-box').slice(0, 3).show();
	$("#loadMore").on('click',function(){

		var _currentProducts=$(".product-box").length;
		var _limit=$(this).attr('data-limit');
		var _total=$(this).attr('data-total');
		if ($(".product-box").length){
		    $("#loadMore").fadeOut();
		}

		// Start Ajax
		$.ajax({
			url:'/load-more-data',
			data:{
				limit:_limit,
				offset:_currentProducts
			},
			dataType:'json',
			beforeSend:function(){
				$("#loadMore").attr('disabled',true);
				$(".load-more-icon").addClass('fa-spin');
			},
			success:function(res){
				$("#filteredProducts").append(res.data);
				$("#loadMore").attr('disabled',false);
				$(".load-more-icon").removeClass('fa-spin');
                $(".product-box").slice(0, 4).show();
				var _totalShowing=$(".product-box").length;
				if(_totalShowing==_total){
					$("#loadMore").remove();
				}
			}
		});
		// End
	});

});