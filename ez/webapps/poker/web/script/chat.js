var sendTime;
var chat;
var message;
$(document).ready(function(){
	$.getJSON("/json?jid=1003", function(local){
		$("#nickname").val(local.host);
	});
//	timedCount();
	$("#inputMessage").click(function(){
		$("#inputMessage").text("");
	});
//	setInterval(function(){$('#time').html(currentTime);},1000);
	$("#send").bind("click", function(){
		message = $("#inputMessage").val();
		$("#inputMessage").val("");
		$.getJSON("/json?jid=1001", {"name":$("#nickname").val(),"message":message}, function(UserList){
			$.each(UserList, function(k, v){
				$("#chatLog").val($("#chatLog").val()+this.name+" "+getTime(this.time)+"\n  "+this.message+"\n");
			});
		});
//		$.ajax({url: "/json?jid=1001", 
//				type: "GET",
//				cache: false, 
//				dataType: "json", 
//				data: {"name":$("#nickname").val(),"message":message},
//				success: function(UserList){
//					$.each(UserList, function(k, v){
//						$("#chatLog").val($("#chatLog").val()+this.name+" "+getTime(this.time)+"\n  "+this.message+"\n");
//					});
//				}, 
//				complete: function(data){
//					$("#chatLog").val($("#chatLog").val()+$("#nickname").val()+" "+getTime()+"\n  "+message+"\n");
//				}
//			});
	});

	$("#reset").click(function(){
		$("#inputMessage").val("");
	});
	$("#getJson").click(function(){
		$.get("/json?jid=1002", {"name":$("#nickname").val()}, function(UserList){
			$.each(UserList, function(k, v){
				$("#chatLog").val($("#chatLog").val()+this.name+" "+getTime(this.time)+"\n  "+this.message+"\n");
			});
		}, "json");
	});
});

function timedCount() {
	$("#getJson").click();
	setTimeout("timedCount()",2000);
};

function currentTime(){
	var d = new Date(),str = '';
	sendTime = d.getTime();
	str += d.getFullYear()+'年';
	str += d.getMonth() + 1+'月';
	str += d.getDate()+'日';
	str += d.getHours()+'时'; 
	str += d.getMinutes()+'分'; 
	str += d.getSeconds()+'秒'; 
	return str;
};

function getTime(time){
	var d;
	if(time == undefined){
		d = new Date();
	}else{
		d = new Date(time);
	}
	var str = '';
	str += d.getHours()+':'; 
	str += d.getMinutes()+':'; 
	str += d.getSeconds(); 
	return str;
};
