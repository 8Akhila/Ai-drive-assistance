/**
 * Triggered when the user opens Drive with the Add-on installed.
 * Shows a search box to type any query (like “give my resume”).
 */
function onDriveOpen(e) {
  return buildMainCard();      // Load the sidebar UI card
}


/**
 * UI — builds the sidebar card with a text field + search button.
 */
function buildMainCard() {
  var card = CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader()
      .setTitle("AI Drive Assistant")
      .setSubtitle("Search anything inside your Drive"))
    .addSection(
      CardService.newCardSection()
        .addWidget(CardService.newTextInput()
          .setFieldName("query")
          .setTitle("Type your question"))
        .addWidget(CardService.newTextButton()
          .setText("Search")
          .setOnClickAction(
            CardService.newAction()
              .setFunctionName("runQuery")
          ))
    );

  return card.build();
}


/**
 * Calls your FastAPI backend with the user query.
 */
function runQuery(e) {
  var query = e.formInput.query;      // Read user input

  // Backend API endpoint
  var url = "http://localhost:8000/query";   // Change to your backend URL if deployed

  var response = UrlFetchApp.fetch(url, {
    "method": "post",
    "contentType": "application/json",
    "payload": JSON.stringify({ query: query })
  });

  var result = JSON.parse(response.getContentText());  // Convert JSON string to JS object

  return buildResultCard(result);      // Show answer & matched files
}
