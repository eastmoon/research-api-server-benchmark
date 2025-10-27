## Declare alias

## Execute script
#
echo "----- Test numeric addition. -----"
curl -X GET http://server/api/add/0/5
echo ""
#
curl -X GET http://server/api/add/5/10
echo ""
#
curl -X GET http://server/api/add/100/50
echo ""
