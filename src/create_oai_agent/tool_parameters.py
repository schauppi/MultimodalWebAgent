parameters_for_input_text = {
    "query": {
        "description": "The query to be used for identifying the input fields and the keys to be sent. This should be a clear and concise description of the input fields and the text values to be entered into them.",
        "examples": [
            "Type 'OpenAI' into the 'Search' input field.",
            "Type example@gmail.com into the 'Email' input field, and type 'securePassword!' into the 'Password' input field.",
            "Enter '123 Main St' into the address field and select 'United States' from the country dropdown."
        ],
        "title": "Query",
        "type": "string",
    }
}

tool_parameters = {
    "input_text": parameters_for_input_text,

}
