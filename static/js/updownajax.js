
	function upvotethis(postid,threadid) {
		//get postid and threadid
		var post_id;
		var thread_id;
		upvotecount="#upvotecount"+postid;
		//get the upvote count id
		$.get('/th/upvote',{post_id: postid, thread_id: threadid}, function(data) {
			data=" "+data;
			$(upvotecount).html(data);
			//send recieve update
		});
	}


	function downvotethis(postid,threadid) {
		var post_id;
		var thread_id;
		upvotecount="#downvotecount"+postid;
		$.get('/th/downvote',{post_id: postid, thread_id: threadid}, function(data) {
			data=" "+data;
			$(upvotecount).html(data);
		});
	}
	
