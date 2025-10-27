## Declare alias

## Execute script
#
echo "----- Test string replace. -----"
curl -X GET http://server/api/str/abcdef12345fedcba/5/z
echo ""
#
curl -X GET http://server/api/str/abcdef12345fedcba/a/_
echo ""
#
curl -X GET http://server/api/str/abcdef12345fedcba/cb/__
echo ""
