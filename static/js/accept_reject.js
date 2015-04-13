
	function acceptthis(projectid,userid) {
		//get postid and threadid
		var project_id;
		var user_id;
		upvotecount="#upvotecount"+postid;
		//get the upvote count id
		$.get('/th/upvote',{project_id: projectid, user_id: userid}, function(data) {
			data=" "+data;
			$(upvotecount).html(data);
			$(upvotecount).html(data);
			$(upvotecount).addClass('disabled')
			$(upvotecount).attr('onclick', '');
			//send recieve update
		});
	}


	function rejectthis(postid,threadid) {
		var post_id;
		var thread_id;
		upvotecount="#downvotecount"+postid;
		$.get('/th/downvote',{post_id: postid, thread_id: threadid}, function(data) {
			data=" "+data;
			console.log(data)
			$(upvotecount).html(data);
			$(upvotecount).html(data);
			$(upvotecount).addClass('disabled')
			$(upvotecount).attr('onclick', '');
		});
	}
	
