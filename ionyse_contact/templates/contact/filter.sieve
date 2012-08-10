if not address :is :domain "from" "example.com" { 
  reject "This address is for internal use only. To contact us, please use contact@example.com";
}else{{% for contact in object_list %}
      redirect "{{ contact.email }}";{% endfor %}
}
