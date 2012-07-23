mongo:
	@mongoimport -d vasir_site -c posts deploy/posts.json
