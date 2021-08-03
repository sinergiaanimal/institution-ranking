<template>
    <div id="message-popup" class="modal fade" tabindex="-1" role="dialog">
        <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
            <div class="modal-content">
                <div class=modal-header>
                    <h1 class="modal-title">
                        Sending a message to
                        <i>{{ institution.name }}</i>
                    </h1>
                    <button type="button" class="close"
                            data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div v-for="message in messages" :key="message.id">
                        <p v-if="message.kind == messageTemplateKind.GOOD"
                        class="alert alert-success">
                            Express your gratitude to <i>{{ institution.name }}</i>
                            for animals-oriented policies
                            <i class="far fa-smile"></i>
                        </p>
                        <p v-else-if="message.kind == messageTemplateKind.BAD"
                        class="alert alert-danger">
                            Express concern to <i>{{ institution.name }}</i>
                            for lack of animals-oriented policies
                            <i class="far fa-frown"></i>
                        </p>

                        <p>{{ message.content }}</p>
                    </div>

                    <h2>
                        Choose a way of contact with
                        <i>{{ institution.name }}</i>
                    </h2>
                    <div v-if="institutionDetail"
                         class="d-flex justify-content-around">
                        <div v-for="email in institutionDetail.emails"
                            :key="email.id">
                            {{ email.address }}
                        </div>
                        <div v-for="sm in institutionDetail.social_media_links"
                            :key="sm.id">
                            {{ sm.kind_name }}:
                            {{ sm.url }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import $ from "jquery";

import { apiUrls, messageTemplateKind } from "./static_data";




export default {

    data () {
        return {
            policyCategories: null,
            messageTemplates: [],
            institution: {scores: {}},
            institutionDetail: null,
            messages: [],
            messageTemplateKind: messageTemplateKind

        }
    },

    methods: {
        showMessagePopup (institution) {
            this.institution = institution;
            this.messages = this.getMessages(institution);
            this.getInstitutionDetail(this.institution.id);

            $('#message-popup').modal('show');
        },

        getMessageTemplates () {
            axios.get(apiUrls.messageTemplates).then((response) => {
                this.messageTemplates = response.data;
            });
        },

        getMessages (institution) {
            return this.messageTemplates.filter(item => {
                return (
                    (
                        item.min_score === null ||
                        institution.scores.total >= item.min_score
                    ) && (
                        item.max_score === null ||
                        institution.scores.total <= item.max_score
                    )
                );
            });
        },

        getInstitutionDetail (institutionId) {
            axios.get(
                `${apiUrls.institutions}${institutionId}/`
            ).then((response) => {
                this.institutionDetail = response.data;
            });
        }
    },

    mounted () {
        this.getMessageTemplates();
    },
};
</script>
