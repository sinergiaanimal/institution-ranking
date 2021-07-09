<template>
    <th scope="col" data-col="name"
        @click="updateOrdering">

        {{ colTitle }}&nbsp;<!--
        --><i v-if="inOrdering(colName)" class="fas fa-sort-down d-inline"></i><!--
        --><i v-else-if="inRevOrdering(colName)" class="fas fa-sort-up d-inline"></i><!--
        --><i v-else class="fas fa-sort d-inline"></i>
    </th>
</template>

<script>
export default {
    props: {
        'colTitle': {
            type: String,
            required: true
        },
        'colName': {
            type: String,
            required: true
        },
        'orderingArray': {
            type: Object,
            required: true
        }
    },

    emits: {
        'orderingChanged': () => {
            return true;
        }
    },

    methods: {
        inOrdering (colName) {
            return this.orderingArray.includes(colName);
        },

        inRevOrdering (colName) {
            return this.orderingArray.includes(`-${colName}`);
        },

        updateOrdering (event) {
            this.$emit('orderingChanged', this.colName)
        }
    }
}
</script>
