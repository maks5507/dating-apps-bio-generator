//
// Created by maks5507 (Maksim Eremeev, maks5507@yandex.ru)
//


const checkUrl = urlText => {
  const pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
    '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
    '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
    '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
  return !!pattern.test(urlText);
};

const checkUrls = () => {
  const urlsSet = urlsInputsIds.map(urlId => {
    return checkUrl($(urlId).val());
  });
  const total = urlsSet.reduce((value, next) => value + next);
  updateBadge('#urls-badge', total);
};

urlsInputsIds.map(urlId => {
  $(document).on('keyup', urlId,
                  () => checkUrls());
});
