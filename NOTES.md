linting 
type checking

`python3 -m venv env` => to create the python virtual environment

`. env/bin/activate` => to run the python virtual environment

any packages in requirements.txt
`pip freeze > requirements.txt`

**functions doc
module doc**

integrate a swagger file?

```graphql
.
├── app
│   ├── __init__.py          # App initialization
│   ├── main.py              # FastAPI app entry point
│   ├── models.py            # Pydantic models for request validation
│   ├── routes.py            # API endpoints (routes)
│   ├── services.py          # Matcher service that encapsulates business logic
│   ├── data
│   │   └── items.json       # Predefined items (static data)
│   └── utils
│       └── similarity.py    # Utility for similarity calculation (encapsulated for reuse)
├── tests
│   ├── __init__.py          # Init for tests package
│   ├── test_routes.py       # Unit tests for the API routes
├── requirements.txt         # Required dependencies
└── README.md                # Instructions
```
