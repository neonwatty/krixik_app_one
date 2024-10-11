require "application_system_test_case"

class SearchTest < ApplicationSystemTestCase
  setup do
    @user = users(:one)
  end

  test "test_1: non-logged in user functionality - search" do
    # visit search_path and assert basic elements exist
    visit search_path
    assert_selector "#navbar"
    assert_selector "#search_results"
    assert_selector "#search-box"

    # fill in search box with nothing, assert that proper no search div is present
    fill_in "search-box", with: ""
    assert_equal "", find("#search-box").value
    assert_selector "#no-search-yet"

    # fill in search box with nonsense text, assert that proper no results div is present
    fill_in "search-box", with: "Sample text"
    assert_equal "Sample text", find("#search-box").value
    assert_selector "#no-search-results"

    # fill in search box with fixture-upload-specific search text, assert that proper results found div is present
    fill_in "search-box", with: "upload_two.png" # for unknown reason only the second fixture upload is searchable in test
    assert_equal "upload_two.png", find("#search-box").value
    assert_selector "#search-results-returned"
  end


  test "test_2: logged in user functionality - search" do
    sign_in @user

    # visit search_path and assert basic elements exist
    visit search_path
    assert_selector "#navbar"
    assert_selector "#search_results"
    assert_selector "#search-box"

    # fill in search box with nothing, assert that proper no search div is present
    fill_in "search-box", with: ""
    assert_equal "", find("#search-box").value
    assert_selector "#no-search-yet"

    # fill in search box with nonsense text, assert that proper no results div is present
    fill_in "search-box", with: "Sample text"
    assert_equal "Sample text", find("#search-box").value
    assert_selector "#no-search-results"

    # fill in search box with fixture-upload-specific search text, assert that proper results found div is present
    fill_in "search-box", with: "upload_two.png"  # for unknown reason only the second fixture upload is searchable in test
    assert_equal "upload_two.png", find("#search-box").value
    assert_selector "#search-results-returned"
  end
end
