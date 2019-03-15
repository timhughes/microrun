<template>
    <v-card class="mx-3">

        <v-card-title>
            <v-icon
        large
        left
        v-bind:color="service.status == 'running' ? 'red':'black'"
      >
        favorite
      </v-icon>
            <span class="title font-weight-light">{{service.displayname}}</span>
        </v-card-title>
        <v-card-actions>
          <v-btn flat color="orange" v-on:click="power_toggle()"><v-icon>power_settings_new</v-icon></v-btn>
          <v-btn flat color="orange">Logs</v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
    export default {
        name: "ServiceCard",
        data: () => ({
            service: null
        }),
        created() {
            fetch('http://localhost:8080/api/v1/services')
                .then(r => r.json())
                .then(json => {
                    this.services = json
                });

        },
        props: {
            service: {}
        },
        methods: {
            power_toggle: function(){
                if (this.service.status =='running') {
                    fetch('http://localhost:8080/services/' + this.service.name + '/stop')
                }else{
                    fetch('http://localhost:8080/services/' + this.service.name + '/start')
                }

            }

        }
    }
</script>

<style scoped>

</style>
