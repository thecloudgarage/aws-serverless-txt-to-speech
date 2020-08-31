for fn in 'PostReader_GetPosts' 'PostReader_NewPosts' 'PostReader_ConvertToAudio'
do
        echo "Removing function $fn"
        aws lambda delete-function --function-name $fn
done
