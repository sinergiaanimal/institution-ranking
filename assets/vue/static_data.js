const apiUrls = {
    institutions: "/api/institutions/",
    policyCategories: "/api/policy-categories/",
    messageTemplates: "/api/message-templates/",
};

const messageTemplateKind = {
    GOOD: 1,
    NEUTRAL: 2,
    BAD: 3,
};

const socialMediaLinkKind = {
    FACEBOOK: 1,
    INSTAGRAM: 2,
    TWITTER: 3,
    LINKEDIN: 4,
    YOUTUBE: 5,
    WEBSITE: 6,
    ANOTHER: 7,
};


export {apiUrls, messageTemplateKind, socialMediaLinkKind};