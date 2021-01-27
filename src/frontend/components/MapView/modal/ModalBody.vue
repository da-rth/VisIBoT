<template>
  <div>
    <b-tab active>
      <template #title>
        <div>
          <b-icon-info-square type="border" small />
          <span class="pl-1">Information</span>
        </div>
      </template>
      <information-tab />
    </b-tab>

    <b-tab>
      <template #title>
        <div>
          <b-icon-flag type="border" small />
          <span class="pl-1">Event Log</span>
        </div>
      </template>
      <event-tab />
    </b-tab>

    <b-tab disabled>
      <template #title>
        <div>
          <b-icon-shield-exclamation type="border" small />
          <span class="pl-1">Malware Analysis</span>
        </div>
      </template>

      <p>I'm a disabled tab!</p>
    </b-tab>
  </div>
</template>
