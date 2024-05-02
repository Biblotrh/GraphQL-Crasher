query = '''
query GetTopUGCs($timeScope: TimeScope!, $gameId: String!, $culture: String!, $contentType: String!, $page: String, $pageSize: Int) {
    topUgcs1: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
    topUgcs2: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
     topUgcs3: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
     topUgcs4: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
    topUgcs5: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
    topUgcs6: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
    topUgcs7: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
    topUgcs8: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
    topUgcs9: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
    topUgcs10: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
    topUgcs11: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
     topUgcs12: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
     topUgcs13: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
     topUgcs14: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
    topUgcs15: topUgcs(input:{gameId: $gameId, culture: $culture, contentType: $contentType, timeScope: $timeScope, page: $page, pageSize: $pageSize}) {
        nextPage
        entries {
            id
            title
            lastEditedDate
            lifecycleStatus
            owner
            type
            commentCount
            privacyStatus
            ...on Movie {
                duration
                views
            }
            reactions {
                reactionTypeId
                count
            }
            resources {
                type
                id
            }
            profile {
                id
                name
                membership {
                    lastTierExpiry
                }
                avatar(preferredGameId: $gameId) {
                    face
                    full
                }
            }
        }
    }
}
'''

variables = {
    "timeScope": "ALL_TIME",
    "gameId": "j68d",
    "culture": "fr-FR",
    "contentType": "ArtBooks",
    "page": "1",
    "pageSize": 500
}