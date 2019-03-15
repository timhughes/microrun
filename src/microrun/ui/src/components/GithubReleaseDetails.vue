<template>
    <div class="text-xs-center">
        <v-menu
            v-model="menu"
            :close-on-content-click="false"
            :nudge-width="200"
            offset-x
        >
            <template v-slot:activator="{ on }">
                <v-btn
                    dark
                    v-on="on"
                >
                    {{ info.tag_name }}
                </v-btn>
            </template>

            <v-card>
                <v-list>
                    <v-list-tile avatar>
                        <v-list-tile-avatar>
                            <img :src="info.author.avatar_url" alt="avatar">
                        </v-list-tile-avatar>

                        <v-list-tile-content>
                            <v-list-tile-title>{{info.author.login }}</v-list-tile-title>
                            <v-list-tile-sub-title>{{ info.published_at}}</v-list-tile-sub-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </v-list>

                <v-divider></v-divider>

                <v-list>
                    <v-list-tile>
                        <v-list-tile-content>
                            <v-list-tile-title>{{ info.name }}</v-list-tile-title>
                            <v-list-tile-sub-title>{{ info.body }}</v-list-tile-sub-title>
                        </v-list-tile-content>
                    </v-list-tile>

                </v-list>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn flat @click="menu = false">Cancel</v-btn>
                </v-card-actions>
            </v-card>
        </v-menu>
    </div>
</template>

<script>
    export default {
        name: "GithubReleaseDetails",

        data() {
            return {
                info: '',
                menu: ''
            }
        },
        created() {
            fetch('https://api.github.com/repos/timhughes/microrun/releases/latest')
                .then(r => r.json())
                .then(json => {
                    this.info = json
                });

        }
    }
</script>

<style scoped>

</style>
