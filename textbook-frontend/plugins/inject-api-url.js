// plugins/inject-api-url.js
module.exports = function (context, options) {
    return {
        name: 'inject-api-url',
        injectHtmlTags() {
            const apiUrl = process.env.REACT_APP_API_URL || '';
            return {
                headTags: [
                    {
                        tagName: 'script',
                        innerHTML: `window.__API_URL__ = '${apiUrl}';`,
                    },
                ],
            };
        },
    };
};
