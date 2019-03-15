<template>
    <v-app id="inspire" dark>
        <v-toolbar app fixed clipped-left>
            <v-toolbar-title>Microrun</v-toolbar-title>
            <v-spacer></v-spacer>
            <GithubReleaseDetails/>
        </v-toolbar>
        <v-content>
            <v-container fluid fill-height>
                <v-layout justify-center align-center>
                    <v-flex shrink>
                        <ServiceCardDashboard/>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-content>
        <v-footer app fixed>
            <v-spacer></v-spacer>
            <span>&copy; 2019 </span>
        </v-footer>
    </v-app>
</template>


<script>

    import GithubReleaseDetails from './components/GithubReleaseDetails'
    import ServiceCardDashboard from './components/ServiceDashboard'

    export default {
        name: 'App',
        components: {
            GithubReleaseDetails,
            ServiceCardDashboard
        },
        data: () => ({
            drawer: null
        }),
        props: {
            source: String
        }
    }
</script>
