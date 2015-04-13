
	function upvotethis(postid,threadid) {
		//get postid and threadid
		var post_id;
		var thread_id;
		upvotecount="#upvotecount"+postid;
		console.log(upvotecount);
		//get the upvote count id
		$.get('/th/upvote',{post_id: postid, thread_id: threadid}, function(data) {
			data=" "+data;
			$(upvotecount).html(data);
			
			//send recieve update
		});
		$(upvotecount).parent().addClass('disabled')
		$(upvotecount).parent().attr('onclick', '');
	}


	function downvotethis(postid,threadid) {
		var post_id;
		var thread_id;
		upvotecount="#downvotecount"+postid;
		$.get('/th/downvote',{post_id: postid, thread_id: threadid}, function(data) {
			data=" "+data;

			$(upvotecount).html(data);
			
		});
		console.log("Hello");
		$(upvotecount).parent().addClass('disabled')
		$(upvotecount).parent.().attr('onclick', '');
	}
	
