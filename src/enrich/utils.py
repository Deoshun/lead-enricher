def categorise_enriched_leads(enriched_leads):
    """ Returns Export Ready Leads Categorised """
    cat_leads = {}
    cat_leads['with_email'] =  []
    cat_leads['with_social_links'] = []
    cat_leads['with_number'] = []
    cat_leads['with_address_only'] = []

    for i in range(len(enriched_leads)):
        lead = enriched_leads[i].to_dict()
        if (lead['emails']):
            cat_leads['with_email'].append(lead)
        elif (lead['socials']):
            cat_leads['with_social_links'].append(lead)
        elif (lead['phone']):
            cat_leads['with_number'].append(lead)
        else:
            cat_leads['with_address_only'].append(lead)

    return cat_leads

