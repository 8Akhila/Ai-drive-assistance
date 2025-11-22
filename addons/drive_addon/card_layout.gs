/**
 * Builds the result UI with:
 * - AI answer
 * - List of matched files/snippets
 */
function buildResultCard(result) {
  var card = CardService.newCardBuilder();

  // Add answer section
  card.addSection(
    CardService.newCardSection()
      .addWidget(CardService.newTextParagraph()
        .setText("<b>AI Answer:</b><br>" + result.answer))
  );

  // Add matched chunks section
  var section = CardService.newCardSection()
      .setHeader("Matched Files");

  result.results.forEach(function(item) {
    var snippet = item.text.substring(0, 150) + "...";   // Short preview snippet

    section.addWidget(
      CardService.newTextParagraph()
        .setText("<b>" + item.file_name + "</b><br>" + snippet)
    );
  });

  card.addSection(section);
  return card.build();
}
