<template>
    <RankingBrowser :cfg="cfg" />
</template>


<script>
import RankingBrowser from './RankingBrowser.vue'

export default {
    name: 'RankingBrowserApp',
    components: {
        RankingBrowser
    },
    props: {
        'cfg': {
            type: Object,
            required: true
        },
    }
}
</script>