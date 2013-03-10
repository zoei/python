var select_cards;
$(document).ready(function(){
	$("#room").hide();
	$("#controlBtn input").hide();
//	test();
	select_cards = new Cards([]);
//	timedCount();
	$(document.body).css({background:"black"});
	var cards = new Cards([1,2,3,4]);
	cards.shuffle().sort();
	for(var c in cards.indexs){
		$(".p1").append(cards.cards[c].html);
	};
	$("#betBtn input").click(function(){
		$("#betBtn input").hide();
		$("#controlBtn input").show();
	});
	$(".p1 img").click(function(){
		$(this).toggleClass("select");
		var cards = new Cards([$(this).attr("id")]);
		if($(this).attr("class") == "select"){
			select_cards.append(cards);
		}else{
			select_cards.remove(cards);
		}
	});
	$("#btn1").click(function(){
//		var selects = $(".select");
		var len = select_cards.size();
		select_cards.get_kind_value();
//		alert(select_cards.kind);
//		for(var i in select_cards.indexs){
//			alert(select_cards.indexs[i]);
//		}
//		$(".dropCards img").remove();
//		for(var c=0;c<selects.size();c++){
//			$(".dropCards").append(selects[c]);
//		}
//		$(".dropCards img").toggleClass("dropCards");
	});
	$("#p200").click(function(){
		$(".name").html($("#c0").attr("id"));
	});
});

function timedCount() {
//	$.getJSON("/user.html", {"age":12}, function(json){
//		  alert(1);
//	});
//	$(".p1").load("/json");
//	setTimeout("timedCount()",1000);
}
function test(){
	a = [1,2,3,4,5,6];
	for(i in a.slice(4)){
		alert(i);
	}
}