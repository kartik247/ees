from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import Institute, Departments, Departmentfloormap
from .serializers import InstituteSerializer, DepartmentSerializer
from ees import settings


@csrf_exempt
def institute_list(request):
    """
    List all institutes, or create a new institute.
    """
    if request.method == 'GET':
        institute = Institute.objects.all()
        serializer = InstituteSerializer(institute[0])
        response = serializer.data
        return JsonResponse(response, safe=False)

    elif request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            institute_name = data.get('instituteName')
            institute_id = Institute.objects.create(name=institute_name)

            for eachdep in data['departments']:
                departmentName = eachdep.get('departmentName')
                dep_id = Departments.objects.create(name=departmentName, institute_id=institute_id)
                for eachfloor in eachdep['floorDetails']:
                    floorNumber = eachfloor.get('floorNumber')
                    numberOfUsers = eachfloor.get('numberOfUsers')
                    dfm = Departmentfloormap(department_id=dep_id, floor_number=floorNumber, num_of_users=numberOfUsers)
                    dfm.save()
            responseMsg = {"message": "Your institute ID is " + str(institute_id.pkid) + ". Please call the below URL to generate configurations for your institute",
                       "url": "http://<IPaddress>:<Port>/api/v1/generateConfig/" + str(institute_id.pkid) + "/"}
            return JsonResponse(responseMsg, safe=False, status=201)
        except:
            return JsonResponse({"ERROR: incorrect data provided"}, safe=False, status=400)


@csrf_exempt
def institute_detail(request, pkid):
    """
    Generate config for an institute or delete an institute.
    """
    try:
        institute = Institute.objects.get(pkid=pkid)
    except Institute.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        list_of_files = []
        dir_path = filepath = str(settings.STATICFILES_DIRS[0]) + '\\configFiles\\'
        core_filename = 'Institute_' + str(pkid) + '_CSW_Config.txt'
        core_hostname = 'hostname CORE1\n'
        basic_config = 'vtp mode transparent\nspanning-tree mode rapid-pvst\nudld enable\nerrdisable recovery cause all\n\nno ip http server\nip http secure-server\nip domain-name cisco.local\nip ssh version 2\nip scp server enable\nline vty 0 15\n\ttransport input ssh\n\ttransport preferred none\n\texit\nusername admin secret cisco\nenable secret cisco\nservice password-encryption\naaa new-model\n\nspanning-tree portfast bpduguard default\n\n'
        vlans = '\nvlan 100\n\tname Management\n'
        interfaces = 'int fa0/0\n\tno shutdown\n'

        department = Departments.objects.filter(institute_id=institute)
        for i in range(len(department)):
            departmentName = department[i].name
            vlans += 'vlan ' + str(10+i) + '\n\tname ' + str(departmentName) + '\n'
            interfaces += 'interface fa0/0.' + str(10+i) + '\n\tencapsulation dot1q ' + str(10+i) + '\n\tip address 10.1.' + str(10+i) + '.1 255.255.255.0\n\n'

            distribution_filename = 'Institute_' + str(pkid) + '_Dep_' + str(departmentName) + '_DSW_Config.txt'
            dist_hostname = 'hostname DISTR' + str(10+i) + '\n'
            int_vlan = 'interface vlan ' + str(10+i) + '\n\tip address 10.1.' + str(10+i) + '.2 255.255.255.0\n\tno shutdown\n\n'
            int_vlan_mgmt = 'interface vlan 100\n\tdescription In-band Management\n\tip address 10.1.100.2 255.255.255.0\n\tno shutdown\n\n'

            floor_details = Departmentfloormap.objects.filter(department_id=department[i])
            dist_int_range = 'interface range GigabitEthernet 0/1-' + str(len(floor_details) + 1) + '\n\tswitchport mode trunk\n\tswitchport trunk encapsulation dot1q \n\tswitchport trunk allowed vlan ' + str(10+i) + ',100 \n\tswitchport trunk native vlan 999 \n\tip arp inspection trust \n\tip dhcp snooping trust \n\tspanning-tree portfast trunk \n\tno shutdown \n\tload-interval 30 \n'
            
            for j in range(len(floor_details)):
                floor_number = floor_details[j].floor_number
                num_of_users = floor_details[j].num_of_users
                access_filename = 'Institute_' + str(pkid) + '_Dep_' + str(departmentName) + '_Floor_' + str(floor_number) + '_ASW_Config.txt'
                access_hostname = 'hostname ASW' + str(10+j) + '\n'
                access_int_to_dist = 'interface GigabitEthernet 0/1\n\tdescription Link to Distribution Layer \n\tswitchport mode trunk\n\tswitchport trunk encapsulation dot1q \n\tswitchport trunk allowed vlan ' + str(10+i) + ',100 \n\tswitchport trunk native vlan 999 \n\tip arp inspection trust \n\tip dhcp snooping trust \n\tspanning-tree portfast trunk \n\tno shutdown \n\tload-interval 30 \n\n'
                access_int_range = 'interface range GigabitEthernet 0/2-' + str(num_of_users + 1) + '\n\tswitchport mode access \n\tswitchport access vlan ' + str(10+i) + ' \n\tswitchport host \n\tip arp inspection limit rate 100 \n\tip dhcp snooping limit rate 100 \n\tswitchport port-security maximum 11 \n\tswitchport port-security \n\tswitchport port-security violation restrict\n\tswitchport port-security aging time 2\n\tswitchport port-security aging type inactivity \n\tip verify source \n\tno shutdown \n\tload-interval 30 \n'

                access_full = access_hostname + basic_config + vlans + '\n' + int_vlan + int_vlan_mgmt + access_int_to_dist + access_int_range
                f = open(dir_path + access_filename, 'w')
                f.write(access_full)
                f.close()
                list_of_files.append('http://<IPaddress>:<Port>/api/v1/fetchConfigFile/' + access_filename + '/')

            dist_full = dist_hostname + basic_config + vlans + '\n' + int_vlan + int_vlan_mgmt + dist_int_range
            f = open(dir_path + distribution_filename, 'w')
            f.write(dist_full)
            f.close()
            list_of_files.append('http://<IPaddress>:<Port>/api/v1/fetchConfigFile/' + distribution_filename + '/')
            
        core_full = core_hostname + basic_config + vlans + '\n' + interfaces
        f = open(dir_path + core_filename, 'w')
        f.write(core_full)
        f.close()
        list_of_files.append('http://<IPaddress>:<Port>/api/v1/fetchConfigFile/' + core_filename + '/')

        response = {"message": "Config files have been successfully generated. Please use the file urls to fetch each file",
                    "file_urls": list_of_files}
        return JsonResponse(response, safe=False)

    elif request.method == 'DELETE':
        institute.delete()
        return HttpResponse(status=204)


def fetchConfigFile(request, filename):
    """
    Fetch the generated config file using the filename
    """
    if request.method == 'GET':
        filepath = str(settings.STATICFILES_DIRS[0]) + '\\configFiles\\' + filename
        #print(filename)
        f = open(filepath, 'r')
        response = HttpResponse(f, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response
