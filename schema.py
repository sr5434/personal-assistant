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
  "name": "order_doordash",
  "description":
  "This function allows you to order food with DoorDash. If a user provides incomplete information, please ask for any missing info before using this function to prevent errors.",
  "parameters": {
    "type": "object",
    "properties": {
      "business_address": {
        "type": "string",
        "description": "The address for the business you want to order from."
      }, "business_name": {
        "type": "string",
        "description": "The name for the business you want to order from."
      }, "business_phone": {
        "type": "string",
        "description": "The phone number for the business you want to order from."
      }, "business_instruct": {
        "type": "string",
        "description": "The instructions for the deliveryperson when picking up the food."
      }, "dropoff_addr": {
        "type": "string",
        "description": "The address to drop the food off at."
      }, "dropoff_name": {
        "type": "string",
        "description": "The name of the business to dropp the food at, if applicable. Return NA if you are not delivering to a business."
      }, "dropoff_num": {
        "type": "string",
        "description": "The phone number for the person/business recieving the food."
      }, "dropoff_instruct": {
        "type": "string",
        "description": "The instructions for dropping off the food."
      }, "num": {
        "type": "string",
        "description": "How many things to order."
      }
    },
    "required": ["business_address", 
                 "business_name",
                  "business_phone",
                  "business_instruct", 
                  "dropoff_addr", "dropoff_name", "dropoff_num", "dropoff_instruct", "num"],
  },
}]