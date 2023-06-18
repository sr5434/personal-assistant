functions = [{
  "name": "get_news",
  "description": "Use this function to get the latest news.",
  "parameters": {
    "type": "object",
    "properties": {
      "N-Results": {
        "type": "string",
        "description": "The number of results. Try to get at least 5."
      }
    },
    "required": ["N-Results"],
  },
}, {
  "name": "get_num_astronauts",
  "description": "Use this function to get the number of astronauts in space.",
  "parameters": {
    "type": "object",
    "properties": {},
    "required": [],
  },
}, {
  "name": "list_astronauts",
  "description":
  "Use this function to get a table of who is in space and what craft they are on.",
  "parameters": {
    "type": "object",
    "properties": {},
    "required": [],
  },
}, {
  "name": "generate_image",
  "description":
  "Use this function to generate an image from a prompt using OpenAI DALL-E. Please note that it returns a URL linking to the image and the URL must be copied verbatim in order for the link to work.",
  "parameters": {
    "type": "object",
    "properties": {
      "prompt": {
        "type": "string",
        "description": "A description of the image to be generated."
      }
    },
    "required": ["prompt"],
  },
  }, {
  "name": "wolfram_alpha",
  "description":
  "This function accesses Wolfram Alpha. Use it when doing any sort of mathematical operation or if you need up to date info.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The query to send to wolfram alpha."
      }
    },
    "required": ["query"],
  },
}]