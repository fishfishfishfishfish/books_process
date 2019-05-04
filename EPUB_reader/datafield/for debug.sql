select sentence.sentence from 
	(contents INNER join content_sentence_relation ON contents.id=content_sentence_relation.content_id)
	INNER JOIN sentence ON content_sentence_relation.sentence_id = sentence.id
	WHERE contents.id = 3;