CREATE TABLE privatemessage (
    id INTEGER PRIMARY KEY,
    content VARCHAR NOT NULL,
    published_at DATETIME NOT NULL
);

- créer table 'message' (sans relations)

- transférer les données de 'privatemessage' vers 'message'
  et de userprivatemessage vers 'message' (sender_id)

INSERT INTO message (id, content, published_at, sender_id)
SELECT pm.id, pm.content, pm.published_at, upm.sender_id
FROM privatemessage as pm JOIN userprivatemessage as upm ON pm.id = upm.private_message_id;


- modifier 'useraccount' + modifier 'message'

- supprimer table 'privatemessage'