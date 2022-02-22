# Team: 50

Members:
- Shashwat Singh
- Venika Shruti
- Tisha Dubey 
- Lokesh Paidi 

# Design Overview 

## Architectural design 

### APIs

- feed: user queries a feed and sends their user token to receive a user specific feed 

### Model 

| Class number | Class state | Class Behaviour |
|----|---------------------------|----------------------|
1 | Represents an article: has full article text, author name, agency name, date, vectorized form | methods: vectorize (to re-vectorize), string_search (to search keywords) |
2 | User: data about the business, export area, export product | getters and setters |

### Sequence Diagram

### Design Rationale 

- Ideally the articles will be stored in an SQL database 
- We need the vectorized form available as well as the actual text (along with the metadata) 
- for the products specific queries, we'll need to do string matching on the keywords of the article. 
- User data will be available from API provided by client, therefore it is good to have a class that is compatible with that. 

