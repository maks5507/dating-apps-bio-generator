const constructData = () => {
  const urls = urlsIds.map(urlId => $(urlId).val())

  const data = {
    'text': urls,
  }

  return data
};

$(document).on("click", submitButtonId, () => {
  $(loadingGifId).fadeIn(0)

  $(resultId).html('')
  const data = constructData()

  data['action'] = 'generation'

  $.ajax({
    type: 'POST',
    url: server,
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify(data),
    success: result => {
      blockSystem()
      $(loadingGifId).fadeOut(0)
      $(resultId).html(result)
    }
  });
  return false;
});
