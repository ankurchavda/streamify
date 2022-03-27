version: 2

sources:
    - name: staging
      database: "{{ env_var('GCP_PROJECT_ID') }}"
      schema: streamify_stg
      tables:
        - name: listen_events
        - name: page_view_events
        - name: auth_events
        - name: songs
        - name: state_codes