<template>
    <v-container grid-list-md text-xs-center>
        <v-layout row wrap>
            <v-flex v-for="service in services">
                    <ServiceCard v-bind:service="service"/>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import ServiceCard from './ServiceCard'

    export default {
        name: "ServiceDashboard",
        components: {
            ServiceCard,
        },
        data: () => ({
            services: null
        }),
        created() {
            fetch('http://localhost:8080/api/v1/services')
                .then(r => r.json())
                .then(json => {
                    this.services = json
                });

        },
        props: {
            source: String
        }
    }
</script>

<style scoped>

</style>
