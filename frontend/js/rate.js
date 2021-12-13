to_block_before_rate = [submitButtonId, ...urlsInputsIds]

const sendRating = () => {
  const rating = getRating()
  console.log(rating)
  unlockSystem()
}

const getRating = () => {
  const rating = $('input[name="rate"]').val()
  return parseInt(rating)
}

const blockSystem = () => {
  $(rateId).fadeIn(0)
  to_block_before_rate.map(item => {
    $(item).attr('disabled', 'disabled')
  })
}

const unlockSystem = () => {
  to_block_before_rate.map(item => {
    $(item).removeAttr('disabled')
  })
  $('input[name=rate]').prop('checked', false)
  $(rateId).fadeOut(0)
}

$(document).on('click', sendRateId, () => sendRating())
